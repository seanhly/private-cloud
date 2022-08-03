from os.path import join, exists, basename
from os import environ, makedirs


MAIN_HOST = "seanhealy.ie"
ADMIN_USERNAME = "sean"
MAIN_EMAIL = f"{ADMIN_USERNAME}@{MAIN_HOST}"

GITHUB_REPO = "seanhly/private-cloud"
GROBID_REPO = "kermitt2/grobid"
CRYPTPAD_REPO = "xwiki-labs/cryptpad"
GITHUB_HOST = "https://github.com/"
RAW_GITHUB_HOST = "https://raw.githubusercontent.com/"
GARAGE_HOST = "https://garagehq.deuxfleurs.fr/"
PROJECT_SOURCE = f"{GITHUB_HOST}{GITHUB_REPO}"
GROBID_SOURCE = f"{GITHUB_HOST}{GROBID_REPO}"
CRYPTPAD_SOURCE = f"{GITHUB_HOST}{CRYPTPAD_REPO}"

GROBID_VERSION = "0.7.1"
GROBID_SOURCE = f"{GROBID_SOURCE}/archive/refs/tags/{GROBID_VERSION}.zip"
GROBID_DIR_NAME = f"grobid-{GROBID_VERSION}"
WORKING_DIR = environ["HOME"]

GROBID_DIR_PATH = join(WORKING_DIR, GROBID_DIR_NAME)
CRYPTPAD_USER = "cryptpad"
CRYPTPAD_UID = 99
CRYPTPAD_GID = 99
CRYPTPAD_LABEL = basename(CRYPTPAD_SOURCE)
CRYPTPAD_USER_DIR = join("/home", CRYPTPAD_USER)
CRYPTPAD_DIR_PATH = join(CRYPTPAD_USER_DIR, CRYPTPAD_LABEL)
GROBID_EXEC_PATH = join(GROBID_DIR_PATH, "gradlew")

USER = environ['USER']
PROJECT_VAR = "/var/private-cloud"
if not exists(PROJECT_VAR):
	makedirs(PROJECT_VAR)
PROJECT_POOL = join(WORKING_DIR, ".private_cloud_pool.json")
PROJECT_NEAREST_SERVER = join(WORKING_DIR, ".private_cloud_nearest")
VULTR_TOKEN_PATH = join(WORKING_DIR, ".vultr_token")
PROJECT_PRIVATE_RSA_KEY = join(WORKING_DIR, ".private_cloud_rsa")
PROJECT_PUBLIC_RSA_KEY = f"{PROJECT_PRIVATE_RSA_KEY}.pub"
VULTR_TOKEN = ""
if exists(VULTR_TOKEN_PATH):
	with open(VULTR_TOKEN_PATH, "r") as f:
		VULTR_TOKEN = f.read().strip()

PROJECT_LABEL = "private-cloud"
EXECUTABLE = f"/usr/bin/{PROJECT_LABEL}"

REDIS_WORKER_NETWORK_DB = 0
REDIS_WORK_QUEUES_DB = 1
GIT_BINARY = "/usr/bin/git"
INSTALL_SCRIPT = "install.sh"
INSTALL_SCRIPT_URL = f"{RAW_GITHUB_HOST}{GITHUB_REPO}/master/{INSTALL_SCRIPT}"
BOOTSTRAP_SCRIPT = f"sh -c \"$(wget {INSTALL_SCRIPT_URL} -O -)\""

COCKROACH_INSTALL_URL = (
	"https://binaries.cockroachdb.com/cockroach-v22.1.4.linux-amd64.tgz"
)
COCKROACH_BINARY_NAME = "cockroach"
COCKROACH_BINARY = join("/usr/local/bin", COCKROACH_BINARY_NAME)
COCKROACH_PORT = 26257
COCKROACH_WEB_PORT = 8080
GARAGE_INSTALL_URL = (
	f"{GARAGE_HOST}_releases/v0.7.2.1/x86_64-unknown-linux-musl/garage"
)
GARAGE_BINARY_NAME = "garage"
GARAGE_BINARY = join("/usr/local/bin", GARAGE_BINARY_NAME)
GARAGE_PORT = 3901
GARAGE_S3_PORT = 3900

TMP_DIR = "/tmp"

TMUX_BINARY = "/usr/bin/tmux"
UFW_BINARY = "/usr/sbin/ufw"
RSYNC_BINARY = "/usr/bin/rsync"
APT_GET_BINARY = "/usr/bin/apt-get"
PACMAN_BINARY = "/usr/bin/pacman"
SYSTEMCTL_BINARY = "/usr/bin/systemctl"
SERVICE_BINARY = "/usr/sbin/service"
REDIS_CLI_BINARY = "/usr/bin/redis-cli"
SSH_BINARY = "/usr/bin/ssh"
SSH_KEYGEN_BINARY = "/usr/bin/ssh-keygen"
SUDO_BINARY = "/usr/bin/sudo"
OLD_NPM_BINARY = "/usr/bin/npm"
NEW_NPM_BINARY = "/usr/local/bin/npm"
NODE_BINARY = "/usr/local/bin/node"
BOWER_BINARY = "/usr/local/bin/bower"
USERADD_BINARY = "/usr/sbin/useradd"
GROUPADD_BINARY = "/usr/sbin/groupadd"
PIP_BINARY = "/usr/bin/pip3"
CERTBOT_BINARY = "/usr/bin/certbot"

SSH_CLIENT = environ.get("SSH_CLIENT", "127.0.0.1").strip().split()[0]

PROJECT_GIT_DIR = "/private-cloud"
PROJECT_ETC_DIR = join(PROJECT_GIT_DIR, "etc")
HOSTNAME_FILE = "/etc/hostname"

CRYPTPAD_CONFIG_SRC = join(PROJECT_GIT_DIR, "config/cryptpad.js")
CRYPTPAD_CONFIG_DST = join(CRYPTPAD_DIR_PATH, "config/config.js")
CRYPTPAD_NGINX_CONFIG_SRC = join(PROJECT_GIT_DIR, "cryptpad.nginx.conf")
CRYPTPAD_NGINX_CONFIG_DST = join("/etc")

ETC_REPLACEMENTS = {
	"main_host": MAIN_HOST,
}

NAMESERVERS = {
	"ns1.seanhealy.cyou",
}
UPDATE_RAPID_DNS_RECORDS_BINARY = "/root/update-rapid-dns-records"