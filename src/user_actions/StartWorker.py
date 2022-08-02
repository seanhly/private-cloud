from typing import Dict, List, Optional, Tuple
from user_actions.ConnectGarageWorkers import ConnectGarageWorkers
from user_actions.UserAction import UserAction
from constants import (
	COCKROACH_BINARY, COCKROACH_BINARY_NAME, COCKROACH_PORT, COCKROACH_WEB_PORT, CRYPTPAD_DIR_PATH, CRYPTPAD_SOURCE,
	GARAGE_BINARY, GARAGE_BINARY_NAME, GROBID_DIR_PATH,
	GROBID_EXEC_PATH,
	TMUX_BINARY
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

	def recognised_options(self):
		return set()

	def arg_options(self):
		return set()

	def obligatory_option_groups(self):
		return []

	def blocking_options(self):
		return []
	
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
				f"{COCKROACH_BINARY} start-single-node {common_cockroach_args}"
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
					f"{COCKROACH_BINARY} start {common_cockroach_args} --join={join_ips}"
				)
			else:
				lowest_ip = min(min(the_network), my_ip)
				if lowest_ip == my_ip:
					cockroach_cmd = (
						f"{COCKROACH_BINARY} start-single-node {common_cockroach_args}"
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
						f"{COCKROACH_BINARY} start {common_cockroach_args} --join={join_ips}"
					)
		services: Dict[str, Tuple[Optional[str], str]] = {
			"grobid": (
				GROBID_DIR_PATH,
				f"/usr/bin/sh {GROBID_EXEC_PATH} run"
			),
			GARAGE_BINARY_NAME: (
				None,
				f"{GARAGE_BINARY} server"
			),
			COCKROACH_BINARY_NAME: (
				None,
				cockroach_cmd
			),
			basename(CRYPTPAD_SOURCE): (
				CRYPTPAD_DIR_PATH,
				"node server.js"
			)
		}
		threads: List[Popen] = []
		print("Running services in TMUX...")
		for name, (cwd, cmd) in services.items():
			if call([TMUX_BINARY, "has-session", "-t", name]) != 0:
				threads.append(
					Popen(
						[TMUX_BINARY, "new-session", "-d", "-s", name, cmd],
						cwd=cwd,
					)
				)
		wait_then_clear(threads)
		ConnectGarageWorkers().execute()
