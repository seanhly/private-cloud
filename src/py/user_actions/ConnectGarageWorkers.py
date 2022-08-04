from typing import List
from user_actions.UserAction import UserAction
from constants import GARAGE_BINARY, GARAGE_PORT, GARAGE_S3_PORT
from subprocess import call
import time
from util.redis_utils import await_garage_id, set_garage_id, get_network
from util.are_ports_online import are_ports_online


class ConnectGarageWorkers(UserAction):
	@classmethod
	def command(cls) -> str:
		return "cgws"

	@classmethod
	def description(cls):
		return "Connect up garage workers."

	def recognised_options(self):
		return set()

	def arg_options(self):
		return set()

	def obligatory_option_groups(self):
		return []

	def blocking_options(self):
		return []
	
	def execute(self) -> None:
		the_network = get_network()
		garage_active_on_ips: List[str] = []
		if the_network:
			for ip in the_network:
				if are_ports_online(ip, (GARAGE_PORT, GARAGE_S3_PORT)):
					garage_active_on_ips.append(ip)
				if len(garage_active_on_ips) == 3:
					break
			if len(garage_active_on_ips) == 0:
				while not garage_active_on_ips:
					time.sleep(0.3)
					for ip in the_network:
						if are_ports_online(ip, (GARAGE_PORT, GARAGE_S3_PORT)):
							garage_active_on_ips.append(ip)
						if len(garage_active_on_ips) == 3:
							break
				while True:
					if are_ports_online(ports=(GARAGE_PORT, GARAGE_S3_PORT)):
						break
					else:
						time.sleep(0.3)
		set_garage_id()
		connected = False
		for ip in garage_active_on_ips:
			try:
				garage_id = await_garage_id(ip)
				if call([
					GARAGE_BINARY,
					"node",
					"connect",
					f"{garage_id}@{ip}:{GARAGE_PORT}"
				]) == 0:
					connected = True
					break
			except Exception:
				pass
		if not connected:
			raise Exception("cannot connect")
