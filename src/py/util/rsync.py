from subprocess import call
from typing import Optional, Union, List
from constants import PROJECT_PRIVATE_RSA_KEY, RSYNC, SSH_BINARY

REMOTE_RSYNC_ARGS = (
	"-e",
	f"{SSH_BINARY} -o  StrictHostKeyChecking=no -o "
	f"PasswordAuthentication=no -i {PROJECT_PRIVATE_RSA_KEY}"
)


def rsync(
	src_dir: Union[str, List[str]],
	dst_dir: str,
	host: Optional[str] = None,
	reverse: bool = False,
	delete_extraneous_files: bool = False,
	user: str = "root",
	chmod: Optional[int] = None,
) -> int:
	if reverse:
		remote_src_paths = (src_dir,) if type(src_dir) == str else src_dir
		src_paths = (
			f"{user}@{host}:{remote_src_path}"
			for remote_src_path in remote_src_paths
		)
		dst_path = dst_dir
	else:
		src_paths = (src_dir,) if type(src_dir) == str else src_dir
		dst_path = (f"{user}@{host}:{dst_dir}" if host else dst_dir)
	args = [
		RSYNC,
		"-Pav",
		*(REMOTE_RSYNC_ARGS if host else ()),
	]
	if delete_extraneous_files:
		args.append("--delete")
	if chmod:
		args += ["--chmod", oct(chmod)[2:]]
	args += src_paths
	args.append(dst_path)
	return call(args)
