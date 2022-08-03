from subprocess import Popen
from arguments.IPArgument import IPArgument
from constants import MAIN_HOST, NAMESERVERS, UPDATE_RAPID_DNS_RECORDS_BINARY
from user_actions.CreateInstanceOnIPs import (
	MAIN_IP_OPTION, CreateInstanceOnIPs, CERTBOT_SUFFIX_OPTION
)
from user_actions.UserAction import UserAction
from cloud.server.Instance import Instance
from cloud.server.Pool import Pool
from cloud.vendors.Vultr import Vultr
import time
from datetime import datetime
from typing import List
from random import choice
from util.ssh_do import ssh_do
from util.wait_then_clear import wait_then_clear
from arguments.OptionArgument import OptionArgument
from arguments.OtherArgument import OtherArgument


class CreateInstance(UserAction):
	@classmethod
	def command(cls) -> str:
		return "new"

	@classmethod
	def description(cls):
		return "Create one or more instances"

	def recognised_options(self):
		return set()

	def arg_options(self):
		return set()

	def obligatory_option_groups(self):
		return []

	def blocking_options(self):
		return []

	def execute(self) -> None:
		current_pool = Pool.load(Vultr)
		count = int(self.query.strip()) if self.query else 1
		new_instances: List[Instance] = []
		for i in range(count):
			new_instances.append(Vultr.create_instance(min_ram=2000))
		start = datetime.now().timestamp()
		incomplete_server = True
		while incomplete_server:
			print(
				f"\rAwaiting activation [{int(datetime.now().timestamp() - start)}s] ",
				end="")
			incomplete_server = False
			i = 0
			while i < len(new_instances) and not incomplete_server:
				instance_state = Vultr.get_instance(new_instances[i].id)
				if (
						not instance_state.main_ip
						or instance_state.main_ip == "0.0.0.0"
						or not instance_state.v6_main_ip
						or instance_state.v6_main_ip == "::"
						or not instance_state.internal_ip
						or instance_state.internal_ip == "0.0.0.0"
						or instance_state.status != "active"
				):
					incomplete_server = True
				else:
					new_instances[i] = instance_state
				i += 1
			time.sleep(0.3)
		print()
		new_instance_ips = {i.main_ip for i in new_instances}
		if current_pool.pool:
			main_ip = None
		else:
			main_ip = choice(tuple(new_instance_ips))
			threads: List[Popen] = []
			from random import choices
			ALPHA_NUMERICAL_LOWERCASE_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"
			certbox_suffix = "".join(
				choices(
					ALPHA_NUMERICAL_LOWERCASE_CHARACTERS, k=3,
				)
			)
			for ns in NAMESERVERS:
				cmd = " ".join([
					UPDATE_RAPID_DNS_RECORDS_BINARY,
					MAIN_HOST,
					main_ip,
					certbox_suffix,
				])
				threads.append(ssh_do(ns, cmd))
			wait_then_clear(threads)
		start = datetime.now().timestamp()
		ssh_closed = True
		while ssh_closed:
			print(
				f"\rAwaiting SSH access [{int(datetime.now().timestamp() - start)}s] ",
				end="")
			ssh_closed = False
			from util.are_ports_online import are_ports_online
			for new_ip in new_instance_ips:
				if not are_ports_online(new_ip, (22,)):
					ssh_closed = True
					time.sleep(0.3)
					break
		print()
		current_pool.add_all(new_instances)
		current_pool.dump()
		CreateInstanceOnIPs(
			[
				IPArgument(new_instance.main_ip)
				for new_instance in new_instances
			] + [
				OptionArgument(f"--{MAIN_IP_OPTION}"), IPArgument(main_ip),
			] + (
				[OptionArgument(f"--{CERTBOT_SUFFIX_OPTION}"), OtherArgument(certbox_suffix)]
				if certbox_suffix else []
			)
		).execute()
