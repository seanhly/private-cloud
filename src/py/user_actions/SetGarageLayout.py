from user_actions.UserAction import UserAction
from typing import Dict, List, Iterable, Tuple
from constants import GARAGE_BINARY, PROJECT_LABEL
from subprocess import Popen, call, check_output
from util.redis_utils import get_region
from util.wait_then_clear import wait_then_clear
from re import fullmatch, search


class SetGarageLayout(UserAction):
	@classmethod
	def command(cls) -> str:
		return "sgl"

	@classmethod
	def description(cls):
		return "Set the disk and datacenter layout of Garage nodes."

	def execute(self) -> None:
		lines: List[str] = []
		for line in check_output([
			GARAGE_BINARY,
			"status"
		]).decode().strip().split("\n")[2:]:
			if not line or line.startswith("="):
				break
			lines.append(line)
		table = (enumerate(line.strip().split()) for line in lines)
		print(table)
		src: Iterable[Tuple[str]] = [
			tuple(part for i, part in row if i in {0, 2})
			for row in table
		]
		src: Iterable[Tuple[str, str]]
		host_and_port_per_id: Dict[str, str] = dict(src)
		print(host_and_port_per_id)
		threads: List[Popen] = []
		for garage_id, host_and_port in host_and_port_per_id.items():
			host, _ = host_and_port.rsplit(":", 1)
			"""
			Sometimes Garage likes to display ipv4 IPs as ipv6 ones.  We can fix
			this, in order to play nicely with Redis.  Redis only appears to
			support ipv4.
			"""
			ipv6_ipv4_match = fullmatch(
				"\\[::ffff:([0-9]+(?:\\.[0-9]+){3})]", host,
			)
			if ipv6_ipv4_match:
				host = ipv6_ipv4_match[1]
			region = get_region(host)
			threads.append(Popen([
				GARAGE_BINARY,
				"layout",
				"assign",
				"-z",
				region,
				"-c",
				str(1),
				garage_id
			]))
		wait_then_clear(threads)
		new_version_match = search(
			"garage layout apply --version ([0-9]+)", 
			check_output([GARAGE_BINARY, "layout", "show"]).decode(),
		)
		if new_version_match:
			version = new_version_match[1]
			Popen([GARAGE_BINARY, "layout", "apply", "--version", version]).wait()
		Popen([GARAGE_BINARY, "bucket", "create", PROJECT_LABEL]).wait()
		if call([GARAGE_BINARY, "key", "info", PROJECT_LABEL]) != 0:
			Popen([GARAGE_BINARY, "key", "new", "--name", PROJECT_LABEL]).wait()
		Popen([
			GARAGE_BINARY,
			"bucket",
			"allow", "--read", "--write",
			PROJECT_LABEL, "--key", PROJECT_LABEL,
		]).wait()
