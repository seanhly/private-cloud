from subprocess import call
from typing import Optional
from constants import PROJECT_PRIVATE_RSA_KEY, RSYNC_BINARY, SSH_BINARY

REMOTE_RSYNC_ARGS = (
	"-e",
	f"{SSH_BINARY} -o  StrictHostKeyChecking=no -o "
	f"PasswordAuthentication=no -i {PROJECT_PRIVATE_RSA_KEY}"
)


def rsync(src_dir: str, dst_dir: str, host: Optional[str] = None) -> int:
	return call([
		RSYNC_BINARY,
		"-Pav",
		*(REMOTE_RSYNC_ARGS if host else ()),
		src_dir,
		(f"root@{host}:{dst_dir}" if host else dst_dir),
	])
