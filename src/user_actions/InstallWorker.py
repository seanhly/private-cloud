from typing import List
from user_actions.UserAction import UserAction
from time import sleep
from constants import (
	APT_GET_BINARY, BOWER_BINARY, CERTBOT_BINARY, COCKROACH_BINARY,
	COCKROACH_BINARY_NAME, COCKROACH_INSTALL_URL, CRYPTPAD_CONFIG_DST,
	CRYPTPAD_CONFIG_SRC, CRYPTPAD_DIR_PATH, CRYPTPAD_GID, CRYPTPAD_SOURCE,
	CRYPTPAD_UID, CRYPTPAD_USER, CRYPTPAD_USER_DIR, ETC_REPLACEMENTS,
	GARAGE_BINARY, GARAGE_INSTALL_URL, GIT_BINARY, GROUPADD_BINARY, MAIN_EMAIL,
	MAIN_HOST, NAMESERVERS, NEW_NPM_BINARY, OLD_NPM_BINARY, PIP_BINARY, PROJECT_SOURCE,
	GROBID_DIR_PATH, GROBID_EXEC_PATH, GROBID_SOURCE, PACMAN_BINARY,
	PROJECT_ETC_DIR, PROJECT_GIT_DIR, SERVICE_BINARY, SSH_CLIENT, SUDO_BINARY,
	SYSTEMCTL_BINARY, TMP_DIR, UFW_BINARY, UPDATE_RAPID_DNS_RECORDS_BINARY, USERADD_BINARY, WORKING_DIR,
)
from os import makedirs, walk, chmod, chown
from os.path import exists, join, basename
from shutil import move, rmtree, copy
from subprocess import Popen, call, PIPE, check_output
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen, Request
import tarfile
from re import sub, findall
from util.wait_then_clear import wait_then_clear


class InstallWorker(UserAction):
	@classmethod
	def command(cls) -> str:
		return "install"

	@classmethod
	def description(cls):
		return "Install worker node software."

	def recognised_options(self):
		return set()

	def arg_options(self):
		return set()

	def obligatory_option_groups(self):
		return []

	def blocking_options(self):
		return []

	def execute(self):
		threads: List[Popen] = [
			Popen([UFW_BINARY, "allow", "from", SSH_CLIENT])
		]
		if exists(APT_GET_BINARY):
			deb_dependencies = [
				"default-jre",
				"tmux",
				"nginx",
				"redis",
				"transmission-daemon",
				"python3-redis",
				"python3-dateparser",
				"npm",
				"certbot",
				"python3-certbot-nginx",
			]

			def deb_install() -> int:
				return call(
					[APT_GET_BINARY, "-y", "install", *deb_dependencies])

			while deb_install() != 0:
				sleep(1)
		elif exists(PACMAN_BINARY):
			pacman_dependencies = [
				"jre11-openjdk-headless",
				"tmux",
				"nginx",
				"redis",
				"transmission-daemon",
				"python-redis",
				"python-requests",
				"python-dateparser",
				"npm",
				"certbot",
				"python-certbot-nginx",
			]
			threads.append(
				Popen([
					PACMAN_BINARY,
					"-S",
					*pacman_dependencies
				])
			)
		pip3_packages = [
			"minio", "grobid-tei-xml",
		]
		npm_packages = [
			"bower", "node", "npm"
		]
		threads.append(Popen([PIP_BINARY, "install", *pip3_packages]))
		threads.append(Popen([OLD_NPM_BINARY, "install", "-g", *npm_packages]))
		if not exists(PROJECT_GIT_DIR):
			threads.append(
				Popen([GIT_BINARY, "clone", PROJECT_SOURCE, PROJECT_GIT_DIR]))
		# Wait for installations, firewall changes, git clone.
		wait_then_clear(threads)
		services = ["nginx", "redis-server", "transmission-daemon"]
		for service in services:
			threads.append(Popen([SYSTEMCTL_BINARY, "enable", service]))
		# Wait for service enabling.
		wait_then_clear(threads)
		print("ETC:", PROJECT_ETC_DIR)
		for src_dir, _, files in walk(PROJECT_ETC_DIR):
			dst_dir = src_dir[len(PROJECT_GIT_DIR):]
			print("DIR", dst_dir)
			if files:
				print("Writing from/to:", src_dir, dst_dir)
				if not exists(dst_dir):
					makedirs(dst_dir)
					print("MKDIR", dst_dir)
				for file in files:
					print(file)
					src_path = join(src_dir, file)
					dst_path = join(dst_dir, file)
					with open(src_path, "r") as src_file:
						content = src_file.read()
						for key, replacement in ETC_REPLACEMENTS.items():
							string = f"{{{{{key}}}}}"
							content = (
								content.replace(string, replacement)
							)
					with open(dst_path, "w") as dst_file:
						dst_file.write(content)
		if not exists(WORKING_DIR):
			makedirs(WORKING_DIR)
		from requests import get
		if not exists(GROBID_EXEC_PATH):
			print("Downloading and unzipping GROBID...")
			ZipFile(
				BytesIO(
					get(GROBID_SOURCE).content
				)
			).extractall(WORKING_DIR)
			print("Setting GROBID permissions...")
			for path, _, files in walk(GROBID_DIR_PATH):
				for file in files:
					file_path = join(path, file)
					chmod(file_path, 0o700)
		if not exists(CRYPTPAD_DIR_PATH):
			Popen([
				GROUPADD_BINARY,
				"-g", str(CRYPTPAD_GID),
				CRYPTPAD_USER
			]).wait()
			Popen([
				USERADD_BINARY,
				"-u", str(CRYPTPAD_UID),
				"-g", str(CRYPTPAD_GID),
				CRYPTPAD_USER
			]).wait()
			if not exists(CRYPTPAD_USER_DIR):
				makedirs(CRYPTPAD_USER_DIR)
				chown(CRYPTPAD_USER_DIR, CRYPTPAD_UID, CRYPTPAD_GID)
			Popen(
				[
					SUDO_BINARY, "-u", CRYPTPAD_USER, GIT_BINARY, "clone",
					CRYPTPAD_SOURCE, CRYPTPAD_DIR_PATH,
				]
			).wait()
			Popen(
				[SUDO_BINARY, "-u", CRYPTPAD_USER, NEW_NPM_BINARY, "install"],
				cwd=CRYPTPAD_DIR_PATH
			).wait()
			Popen(
				[SUDO_BINARY, "-u", CRYPTPAD_USER, BOWER_BINARY, "install"],
				cwd=CRYPTPAD_DIR_PATH
			).wait()
			if not exists(CRYPTPAD_CONFIG_DST):
				copy(CRYPTPAD_CONFIG_SRC, CRYPTPAD_CONFIG_DST)
			Popen([SERVICE_BINARY, "nginx", "stop"]).wait()
			Popen([UFW_BINARY, "allow", "80"]).wait()
			Popen([
				CERTBOT_BINARY, "certonly", "--standalone",
				"-d", f"docs.{MAIN_HOST},secure-docs.{MAIN_HOST}",
				"-m", MAIN_EMAIL, "--agree-tos",
			]).wait()
			for ufw_id in reversed(
				sorted(
					int(i)
					for i in findall(
						"(?:^|\n)\\[\s*(\d+)]\s*80\s*",
						check_output([UFW_BINARY, "status", "numbered"]).decode(),
					)
				)
			):
				p = Popen(
					[UFW_BINARY, "delete", str(ufw_id)],
					stdin=PIPE,
				)
				text: AnyStr = bytes("y", encoding="utf8")
				p.stdin.write(text)
				p.wait()
			Popen([SERVICE_BINARY, "nginx", "start"]).wait()
		if not exists(COCKROACH_BINARY):
			print("Downloading and untarring CockroachDB...")
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
				cockroach_extracted_dir_path, COCKROACH_BINARY_NAME
			)
			move(cockroach_binary_src, COCKROACH_BINARY)
			rmtree(cockroach_extracted_dir_path)
			chmod(COCKROACH_BINARY, 0o700)
		if not exists(GARAGE_BINARY):
			print("Downloading Garage...")
			with open(GARAGE_BINARY, "wb") as f:
				f.write(get(GARAGE_INSTALL_URL).content)
			chmod(GARAGE_BINARY, 0o700)
		rmtree(PROJECT_GIT_DIR)
		for service in services:
			threads.append(Popen([SERVICE_BINARY, service, "restart"]))
		# Wait for service starts.
		wait_then_clear(threads)