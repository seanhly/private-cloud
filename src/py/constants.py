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
HOME_DIR = environ["HOME"]
WORKING_DIR = HOME_DIR

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
EXECUTABLE = join("/usr/bin", PROJECT_LABEL)
LOCAL_EXECUTABLE = join(HOME_DIR, "Scripts", PROJECT_LABEL)

REDIS_WORKER_NETWORK_DB = 0
REDIS_WORK_QUEUES_DB = 1
GIT = "/usr/bin/git"
INSTALL_SCRIPT = "install.sh"
INSTALL_SCRIPT_URL = f"{RAW_GITHUB_HOST}{GITHUB_REPO}/master/{INSTALL_SCRIPT}"
BOOTSTRAP_SCRIPT = f"sh -c \"$(wget {INSTALL_SCRIPT_URL} -O -)\""

COCKROACH_INSTALL_URL = (
	"https://binaries.cockroachdb.com/cockroach-v22.1.4.linux-amd64.tgz"
)
COCKROACH_BINARY_NAME = "cockroach"
COCKROACH = join("/usr/local/bin", COCKROACH_BINARY_NAME)
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
UFW = "/usr/sbin/ufw"
RSYNC = "/usr/bin/rsync"
CHOWN = "/usr/bin/chown"
APT_GET = "/usr/bin/apt-get"
PACMAN = "/usr/bin/pacman"
SYSTEMCTL = "/usr/bin/systemctl"
SERVICE = "/usr/sbin/service"
REDIS_CLI_BINARY = "/usr/bin/redis-cli"
SSH_BINARY = "/usr/bin/ssh"
SSH_KEYGEN_BINARY = "/usr/bin/ssh-keygen"
SUDO = "/usr/bin/sudo"
OLD_NPM = "/usr/bin/npm"
NEW_NPM = "/usr/local/bin/npm"
NODE = "/usr/local/bin/node"
BOWER = "/usr/local/bin/bower"
USERADD = "/usr/sbin/useradd"
GROUPADD = "/usr/sbin/groupadd"
PIP = "/usr/bin/pip3"
CERTBOT_BINARY = "/usr/bin/certbot"
KILLALL = "/usr/bin/killall"
UPDATE_RAPID_DNS_RECORDS_BINARY = "/root/update-rapid-dns-records"

PROJECT_GIT_DIR = "/private-cloud"
PROJECT_CONFIGS_DIR = join(PROJECT_GIT_DIR, "configs")
HOSTNAME_FILE = "/etc/hostname"
CRYPTPAD_CONFIG_SRC = join(PROJECT_GIT_DIR, "config/config.js")
CRYPTPAD_CONFIG_DST = join(CRYPTPAD_DIR_PATH, "config/config.js")
NAMESERVERS = {
	"ns1.seanhealy.cyou",
}
SUPPORTED_SUBDOMAINS = ("docs", "secure-docs", "meet", "www")
PHP_PLUGIN = "php8.1-fpm"
DEB_DEPENDENCIES = [
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
	"fail2ban",
	PHP_PLUGIN,
]
PACMAN_DEPENDENCIES = [
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
	"fail2ban",
	PHP_PLUGIN,
]
SMTP_PORT = 587
PIP_PACKAGES = ["minio", "grobid-tei-xml"]
NPM_PACKAGES = ["bower", "node", "npm"]
NATIVE_SERVICES = [
	"nginx",
	"redis-server",
	"transmission-daemon",
	PHP_PLUGIN,
]
WEBHOSTING_DIR = "/srv"
WEBSITES_DIR = join(PROJECT_GIT_DIR, "src/php")
ALPHA_NUMERICAL_LOWERCASE_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"
# Add git repos for importing
IMPORT_GIT_REPOS = [
	"https://github.com/seanhly/private-cloud",
	"https://github.com/seanhly/phd",
	"https://github.com/seanhly/docmuch",
]
GIT_USER = "git"
GIT_USER_HOME_DIR = f"/home/{GIT_USER}"
GIT_SSH_DIR = join(GIT_USER_HOME_DIR, ".ssh")
GIT_SSH_AUTHORISED_KEYS_FILE = join(GIT_SSH_DIR, "authorized_keys")
ROOT_SSH_AUTHORISED_KEYS_FILE = join(HOME_DIR, ".ssh/authorized_keys")
CRYPTPAD_SSH_DIR = join(CRYPTPAD_USER_DIR, ".ssh")
CRYPTPAD_SSH_AUTHORISED_KEYS_FILE = join(CRYPTPAD_SSH_DIR, "authorized_keys")

CRYPTPAD_DATA_PATH = join(CRYPTPAD_DIR_PATH, "data")
CRYPTPAD_FILE_PATH = join(CRYPTPAD_DIR_PATH, "datastore")
CRYPTPAD_ARCHIVE_PATH = join(CRYPTPAD_DATA_PATH, "archive")
CRYPTPAD_PIN_PATH = join(CRYPTPAD_DATA_PATH, "pins")
CRYPTPAD_TASK_PATH = join(CRYPTPAD_DATA_PATH, "tasks")
CRYPTPAD_BLOCK_PATH = join(CRYPTPAD_DIR_PATH, "block")
CRYPTPAD_BLOB_PATH = join(CRYPTPAD_DIR_PATH, "blob")
CRYPTPAD_BLOB_STAGING_PATH = join(CRYPTPAD_DATA_PATH, "blobstage")
CRYPTPAD_DECREE_PATH = join(CRYPTPAD_DATA_PATH, "decrees")
CRYPTPAD_LOG_PATH = join(CRYPTPAD_DATA_PATH, "logs")

ETC_REPLACEMENTS = {
	"main_host": MAIN_HOST,
	"main_email": MAIN_EMAIL,
	"websites_dir": "/srv",
	"php_plugin": PHP_PLUGIN,
	# This makes it easier for people (mainly me) to connect to my git daemon.
	# The SMTP is less likely to be blocked than GIT daemon's 9418.
	"git_backport": SMTP_PORT,
	"cryptpad_file_path": CRYPTPAD_FILE_PATH,
	"cryptpad_archive_path": CRYPTPAD_ARCHIVE_PATH,
	"cryptpad_pin_path": CRYPTPAD_PIN_PATH,
	"cryptpad_task_path": CRYPTPAD_TASK_PATH,
	"cryptpad_block_path": CRYPTPAD_BLOCK_PATH,
	"cryptpad_blob_path": CRYPTPAD_BLOB_PATH,
	"cryptpad_blob_staging_path": CRYPTPAD_BLOB_STAGING_PATH,
	"cryptpad_decree_path": CRYPTPAD_DECREE_PATH,
	"cryptpad_log_path": CRYPTPAD_LOG_PATH,
}
BACKUP_CRYPTPAD_DIRS = {
	CRYPTPAD_DATA_PATH,
	CRYPTPAD_FILE_PATH,
	CRYPTPAD_BLOCK_PATH,
	CRYPTPAD_BLOB_PATH,
}
CRYPTPAD_BACKUP_DIR = join(HOME_DIR, "cryptpad")
