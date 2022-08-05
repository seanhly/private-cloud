from typing import Dict, List, Optional, Tuple
from user_actions.ConnectGarageWorkers import ConnectGarageWorkers
from user_actions.UserAction import UserAction
from constants import (
	COCKROACH, COCKROACH_BINARY_NAME, COCKROACH_PORT, COCKROACH_WEB_PORT,
	CRYPTPAD_DIR_PATH, CRYPTPAD_SOURCE, CRYPTPAD_USER, GARAGE_BINARY,
	GARAGE_BINARY_NAME, GROBID_DIR_PATH, GROBID_EXEC_PATH, SUDO,
	TMUX_BINARY,
)
from subprocess import Popen, call
from util.redis_utils import get_public_ipv4
from util.wait_then_clear import wait_then_clear
from util.are_ports_online import are_ports_online
import time
from os.path import basename


class StartWorker(UserAction):
	@classmethod
	def command(cls) -> str:
		return "start"

	@classmethod
	def description(cls):
		return "Start worker node."

	def special_services(self) -> Dict[str, Tuple[str, str, str]]:
		return {}
	
	def execute(self) -> None:
		my_ip = get_public_ipv4()
		common_cockroach_args = ' '.join([
			"--insecure",
			f"--advertise-host={my_ip}"
		])
		from util.redis_utils import get_network
		the_network = get_network()
		# If we have no neighbours, then we start CockroachDB as a single node.
		# More nodes can join later.
		if not the_network:
			cockroach_cmd = (
				f"{COCKROACH} start-single-node {common_cockroach_args}"
			)
		else:
			cockroach_active_on_ips: List[str] = []
			for ip in the_network:
				if are_ports_online(ip, (COCKROACH_PORT, COCKROACH_WEB_PORT)):
					cockroach_active_on_ips.append(ip)
				if len(cockroach_active_on_ips) == 3:
					break
			if len(cockroach_active_on_ips) > 0:
				join_ips = ','.join(cockroach_active_on_ips)
				cockroach_cmd = (
					f"{COCKROACH} start {common_cockroach_args} --join={join_ips}"
				)
			else:
				lowest_ip = min(min(the_network), my_ip)
				if lowest_ip == my_ip:
					cockroach_cmd = (
						f"{COCKROACH} start-single-node {common_cockroach_args}"
					)
				else:
					while not cockroach_active_on_ips:
						time.sleep(0.3)
						for ip in the_network:
							if are_ports_online(
								ip, (COCKROACH_PORT, COCKROACH_WEB_PORT)
							):
								cockroach_active_on_ips.append(ip)
							if len(cockroach_active_on_ips) == 3:
								break
					join_ips = ','.join(cockroach_active_on_ips)
					cockroach_cmd = (
						f"{COCKROACH} start {common_cockroach_args} --join={join_ips}"
					)
		services: Dict[str, Tuple[Optional[str], str]] = {
			"grobid": (
				GROBID_DIR_PATH,
				None,
				f"/usr/bin/sh {GROBID_EXEC_PATH} run"
			),
			GARAGE_BINARY_NAME: (
				None,
				None,
				f"{GARAGE_BINARY} server"
			),
			COCKROACH_BINARY_NAME: (
				None,
				None,
				cockroach_cmd
			),
			**self.special_services()
		}
		threads: List[Popen] = []
		print("Running services in TMUX...")
		for name, (cwd, user, cmd) in services.items():
			sudo_prefix = [SUDO, "-u", user] if user else []
			if call([*sudo_prefix, TMUX_BINARY, "has-session", "-t", name]) != 0:
				threads.append(
					Popen(
						[
							*sudo_prefix,
							TMUX_BINARY, "new-session", "-d", "-s", name, cmd,
						],
						cwd=cwd,
					)
				)
		wait_then_clear(threads)
		ConnectGarageWorkers().execute()
