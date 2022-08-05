from enum import Enum
from typing import AnyStr, List
from user_actions.UserAction import UserAction
from util.group_exists import group_exists
from util.user_exists import user_exists
from multiprocessing.pool import ThreadPool
from time import sleep
from constants import (
	APT_GET, BOWER, CERTBOT_BINARY, COCKROACH, COCKROACH_BINARY_NAME,
	COCKROACH_INSTALL_URL, CRYPTPAD_CONFIG_DST, CRYPTPAD_CONFIG_SRC,
	CRYPTPAD_DIR_PATH, CRYPTPAD_GID, CRYPTPAD_SOURCE, CRYPTPAD_UID,
	CRYPTPAD_USER, CRYPTPAD_USER_DIR, ETC_REPLACEMENTS, GARAGE_BINARY,
	GARAGE_INSTALL_URL, GIT, GROUPADD, MAIN_EMAIL, MAIN_HOST, NEW_NPM,
	OLD_NPM, PIP, PROJECT_SOURCE, GROBID_DIR_PATH, GROBID_SOURCE, PACMAN,
	PROJECT_ETC_DIR, PROJECT_GIT_DIR, SERVICE, SUDO, SYSTEMCTL, TMP_DIR, UFW,
	USERADD, WORKING_DIR, SUPPORTED_SUBDOMAINS, KILLALL, DEB_DEPENDENCIES,
	PACMAN_DEPENDENCIES, WEBHOSTING_DIR, WEBSITES_DIR, NATIVE_SERVICES,
	NPM_PACKAGES, PIP_PACKAGES, IMPORT_GIT_REPOS,
)
from os import makedirs, walk, chmod, chown, listdir, environ
from os.path import exists, join, basename
from shutil import move, rmtree, copy
from subprocess import Popen, call, PIPE, check_output
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen, Request
import tarfile
from re import sub, findall
from user_actions.CreateInstanceOnIPs import CERTBOT_SUFFIX_OPTION
from util.rsync import rsync


CRYPTPAD_SUDO = (SUDO, "-u", CRYPTPAD_USER)
INSTAL = "install"


def download_and_extract_grobid(**_):
	from requests import get
	ZipFile(
		BytesIO(
			get(GROBID_SOURCE).content
		)
	).extractall(WORKING_DIR)
	return True


def allow_executing_grobid(**_):
	for path, _, files in walk(GROBID_DIR_PATH):
		for file in files:
			file_path = join(path, file)
			chmod(file_path, 0o700)
	return True


def create_cryptpad_group(**_):
	return (
		group_exists(CRYPTPAD_USER)
		or call([GROUPADD, "-g", str(CRYPTPAD_GID), CRYPTPAD_USER]) == 0
	)


def create_cryptpad_user(**_):
	return (
		user_exists(CRYPTPAD_USER)
		or call([
			USERADD,
			"-u", str(CRYPTPAD_UID), "-g", str(CRYPTPAD_GID), CRYPTPAD_USER
		]) == 0
	)


def create_cryptpad_dir(**_):
	makedirs(CRYPTPAD_USER_DIR)
	return True


def chown_cryptpad_dir(**_):
	chown(CRYPTPAD_USER_DIR, CRYPTPAD_UID, CRYPTPAD_GID)
	return True


def clone_cryptpad_git(**_):
	git_cmd = (GIT, "clone", CRYPTPAD_SOURCE, CRYPTPAD_DIR_PATH)
	return call([*CRYPTPAD_SUDO, *git_cmd]) == 0


def install_cryptpad_npm_dependencies(**_):
	return call([*CRYPTPAD_SUDO, NEW_NPM, INSTAL], cwd=CRYPTPAD_DIR_PATH) == 0


def install_cryptpad_bower_dependencies(**_):
	return call([*CRYPTPAD_SUDO, BOWER, INSTAL], cwd=CRYPTPAD_DIR_PATH) == 0


def copy_cryptpad_configs_to_dst(**_):
	copy(CRYPTPAD_CONFIG_SRC, CRYPTPAD_CONFIG_DST)
	return True


def import_git_repos(**_):
	for repo in IMPORT_GIT_REPOS:
		repo_canonical_name = basename(repo)
		if not repo_canonical_name.lower().endswith(".git"):
			repo_canonical_name += ".git"


def download_garage_binary(**_):
	with open(GARAGE_BINARY, "wb") as f:
		from requests import get
		f.write(get(GARAGE_INSTALL_URL).content)
	return True


def allow_garage_binary_execution(**_):
	chmod(GARAGE_BINARY, 0o700)
	return True


def download_and_install_cockroach(**_):
	req = Request(COCKROACH_INSTALL_URL)
	with urlopen(req) as f:
		with tarfile.open(fileobj=f, mode='r|*') as tar:
			# The tar appears to contain a directory resembling the
			# final part of the URL.
			cockroach_extracted_dir_name = sub(
				"(\\.[a-zA-Z]+)+$",
				"",
				basename(COCKROACH_INSTALL_URL),
			)
			tar.extractall(TMP_DIR)
	cockroach_extracted_dir_path = join(
		TMP_DIR, cockroach_extracted_dir_name
	)
	cockroach_binary_src = join(
		cockroach_extracted_dir_path,
		COCKROACH_BINARY_NAME
	)
	move(cockroach_binary_src, COCKROACH)
	rmtree(cockroach_extracted_dir_path)
	chmod(COCKROACH, 0o700)
	return True


def stop_nginx(**_):
	return call([SERVICE, "nginx", "stop"]) == 0


def allow_80(**_):
	return call([UFW, "allow", "80"]) == 0


def request_ssl_certs(**kwargs):
	supported_subdomains = list(SUPPORTED_SUBDOMAINS)
	if CERTBOT_SUFFIX_OPTION in kwargs:
		supported_subdomains.append(
			f"certbot-{kwargs[CERTBOT_SUFFIX_OPTION]}"
		)
	comma_separated_domains = ",".join(
		f"{subdomain}.{MAIN_HOST}"
		for subdomain in supported_subdomains
	)
	return call([
		CERTBOT_BINARY, "--nginx", "--agree-tos", "-m", MAIN_EMAIL,
		"-d", comma_separated_domains,
	]) == 0


def disallow_80(**_):
	for ufw_id in reversed(
		sorted(
			int(i)
			for i in findall(
				"(?:^|\n)\\[\\s*(\\d+)]\\s*80\\s*",
				check_output([UFW, "status", "numbered"]).decode(),
			)
		)
	):
		p = Popen(
			[UFW, "delete", str(ufw_id)],
			stdin=PIPE,
		)
		text: AnyStr = bytes("y\n", encoding="utf8")
		p.stdin.write(text)
		p.stdin.close()
		p.wait()
	return True


def kill_certbot_nginx_worker(**_):
	return call([KILLALL, "nginx"]) == 0


def start_nginx(**_):
	return call([SERVICE, "nginx", "start"]) == 0


def make_working_dir(**_):
	if not exists(WORKING_DIR):
		makedirs(WORKING_DIR)
	return True


def sync_etc(**kwargs) -> int:
	etc_replacements = dict(ETC_REPLACEMENTS)
	if CERTBOT_SUFFIX_OPTION in kwargs:
		etc_replacements.update(
			dict(certbot_suffix=kwargs[CERTBOT_SUFFIX_OPTION])
		)
	for src_dir, _, files in walk(PROJECT_ETC_DIR):
		dst_dir = src_dir[len(PROJECT_GIT_DIR):]
		if files:
			if not exists(dst_dir):
				makedirs(dst_dir)
			for file in files:
				src_path = join(src_dir, file)
				dst_path = join(dst_dir, file)
				with open(src_path, "r") as src_file:
					content = src_file.read()
					for key, replacement in etc_replacements.items():
						string = f"{{{{{key}}}}}"
						content = (
							content.replace(string, replacement)
						)
				with open(dst_path, "w") as dst_file:
					dst_file.write(content)
	return True


def sync_websites(**_):
	# Copy website data to appropriate location.
	for website in listdir(WEBSITES_DIR):
		if rsync(
			src_dir=join(WEBSITES_DIR, website),
			dst_dir=WEBHOSTING_DIR,
		) != 0:
			return False
	return True


def deb_install() -> int:
	return call([APT_GET, "-y", "install", *DEB_DEPENDENCIES]) == 0


def install_linux_packages(**_):
	if exists(APT_GET):
		tries = 120
		while tries != 0 and deb_install() != 0:
			sleep(1)
			tries -= 1
		return tries != 0
	elif exists(PACMAN):
		return call([PACMAN, "-S", *PACMAN_DEPENDENCIES]) == 0
	return False


def install_pip_packages(**_):
	return call([PIP, "install", *PIP_PACKAGES]) == 0


def install_npm_packages(**_):
	return call([OLD_NPM, "install", "-g", *NPM_PACKAGES]) == 0


def clone_project_git(**_):
	return (
		exists(PROJECT_GIT_DIR)
		or call([GIT, "clone", PROJECT_SOURCE, PROJECT_GIT_DIR]) == 0
	)


def enable_systemd_services():
	return call([SYSTEMCTL, "enable", *NATIVE_SERVICES]) == 0


def restart_systemd_services():
	return call([SYSTEMCTL, "restart", *NATIVE_SERVICES]) == 0


def allow_access_from_ssh_client():
	return call([
		UFW, "allow", "from",
		environ.get("SSH_CLIENT", "127.0.0.1").strip().split()[0],
	]) == 0


RECIPE = (
	{
		install_linux_packages,
		allow_access_from_ssh_client,
	},
	{
		install_pip_packages,
		install_npm_packages,
		clone_project_git,
	},
	enable_systemd_services,
	sync_etc,
	make_working_dir,
	{
		(
			download_and_extract_grobid,
			allow_executing_grobid,
		),
		(
			create_cryptpad_group,
			create_cryptpad_user,
			create_cryptpad_dir,
			chown_cryptpad_dir,
			clone_cryptpad_git,
			install_cryptpad_npm_dependencies,
			install_cryptpad_bower_dependencies,
			copy_cryptpad_configs_to_dst,
		),
		download_and_install_cockroach,
		(
			download_garage_binary,
			allow_garage_binary_execution,
		),
	},
	# Install certbot
	stop_nginx,
	allow_80,
	request_ssl_certs,
	disallow_80,
	kill_certbot_nginx_worker,
	# Restart services
	restart_systemd_services,
)


def await_breadcrumbs(breadcrumbs):
	if type(breadcrumbs) == tuple:
		i = 0
		for step in breadcrumbs:
			step_result = await_breadcrumbs(step)
			if not step_result:
				return i
			elif type(step_result) != bool:
				return i, step_result
			i += 1
		return True
	elif type(breadcrumbs) == dict:
		successful_breadcrumbs = {}
		for step, sub_breadcrumbs in breadcrumbs.items():
			step_result = await_breadcrumbs(sub_breadcrumbs)
			if step_result:
				successful_breadcrumbs[step] = step_result
		if all(
			type(v) == bool for v in successful_breadcrumbs.values()
		):
			return True
		return successful_breadcrumbs
	else:
		return breadcrumbs.get()


class InstallWorker(UserAction):
	pool: ThreadPool
	recipe = RECIPE

	def execute_installation(self, recipe):
		if type(recipe) == tuple:
			i = 0
			for step in recipe:
				breadcrumb_promises = self.execute_installation(step)
				breadcrumbs = await_breadcrumbs(breadcrumb_promises)
				if not breadcrumbs:
					return i
				elif type(breadcrumbs) != bool:
					return i, breadcrumbs
				i += 1
			return True

		elif type(recipe) == set:
			return {
				step: self.execute_installation(step)
				for step in recipe
			}
		else:
			kwargs = self.options if self.options else {}
			return self.pool.apply_async(recipe, kwds=kwargs)

	@classmethod
	def command(cls) -> str:
		return "install"

	@classmethod
	def description(cls):
		return "Install worker node software."

	def recognised_options(self):
		return {CERTBOT_SUFFIX_OPTION}

	def arg_options(self):
		return {CERTBOT_SUFFIX_OPTION}

	def obligatory_option_groups(self):
		return []

	def blocking_options(self):
		return []

	def execute(self):
		self.pool = ThreadPool(processes=1)
		breadcrumbs = self.execute_installation(RECIPE)
		print(breadcrumbs)
