from subprocess import PIPE, Popen
from typing import Iterable, List, Optional, Union, AnyStr
from constants import PROJECT_PRIVATE_RSA_KEY, SSH_BINARY

SSH_ARGS = (
	SSH_BINARY,
	"-o",
	"StrictHostKeyChecking=no",
	"-o",
	"PasswordAuthentication=no",
	"-i",
	PROJECT_PRIVATE_RSA_KEY,
)


def ssh_do(
	host: str,
	things: Union[Iterable[str], str],
	threads: Optional[List[Popen]] = None,
	stdin: Optional[Union[Iterable[str], str]] = None,
	stdout: bool = False
) -> Optional[Popen]:
	if type(things) == str:
		cmd = things
	else:
		cmd = " && ".join(things)
	if cmd:
		kwargs = {}
		if stdin:
			kwargs["stdin"] = PIPE
		if stdout:
			kwargs["stdout"] = PIPE
		args = [*SSH_ARGS, f"root@{host}", cmd]
		p = Popen(args, **kwargs)
		if stdin:
			if type(stdin) == str:
				text: AnyStr = bytes(stdin, encoding="utf8")
				p.stdin.write(text)
			else:
				for line in stdin:
					text: AnyStr = bytes(f"{line}\n", encoding="utf8")
					p.stdin.write(text)
			p.stdin.close()
		if threads is not None:
			threads.append(p)
		else:
			return p
