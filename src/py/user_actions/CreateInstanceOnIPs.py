from subprocess import Popen
from user_actions.StartMainWorker import StartMainWorker
from user_actions.StartWorker import StartWorker
from user_actions.UserAction import UserAction
from cloud.server.Pool import Pool
from cloud.vendors.Vultr import Vultr
from constants import UFW
from typing import List
from constants import BOOTSTRAP_SCRIPT
from util.ssh_do import ssh_do
from util.wait_then_clear import wait_then_clear
from util.redis_utils import extend_network, set_region_and_public_ipv4


MAIN_IP_OPTION = "main-ip"
CERTBOT_SUFFIX_OPTION = "certbot-suffix"


class CreateInstanceOnIPs(UserAction):
	@classmethod
	def command(cls) -> str:
		return "new-2"

	@classmethod
	def description(cls):
		return "Set up an instance on a pre-created IP."

	def recognised_options(self):
		return {MAIN_IP_OPTION, CERTBOT_SUFFIX_OPTION}

	def arg_options(self):
		return {MAIN_IP_OPTION, CERTBOT_SUFFIX_OPTION}
	
	def execute(self) -> None:
		if self.options and MAIN_IP_OPTION in self.options:
			main_ip = self.options[MAIN_IP_OPTION]
		else:
			main_ip = None
		if self.options and CERTBOT_SUFFIX_OPTION in self.options:
			certbot_suffix = self.options[CERTBOT_SUFFIX_OPTION]
		else:
			certbot_suffix = None
		# New IPs are fed in as arguments.
		# Details for these IPs are then pulled from the Pool cache.
		all_instances = Pool.load(Vultr).pool
		new_instance_ips = {a.ip for a in self.ip_arguments}
		new_instances = [
			instance
			for instance in all_instances
			if instance.main_ip in new_instance_ips
		]
		previous_instances = [
			instance
			for instance in all_instances
			if instance.main_ip not in new_instance_ips
		]
		previous_instance_ips = {i.main_ip for i in previous_instances}
		threads: List[Popen] = []
		# Bootstrap a system onto each worker.
		for new_ip in new_instance_ips:
			kwargs = dict(stdin=certbot_suffix) if certbot_suffix else {}
			threads.append(ssh_do(new_ip, BOOTSTRAP_SCRIPT, **kwargs))
		wait_then_clear(threads)
		# New workers can now reach pre-existing workers.
		# <---|
		for previous_ip in previous_instance_ips:
			ssh_do(previous_ip, (
				f"{UFW} allow from {new_ip}"
				for new_ip in new_instance_ips
			), threads)
		# Pre-existing workers can now reach new workers and each other.
		# a) |--->
		# b) | <-->
		for new_ip in new_instance_ips:
			ssh_do(new_ip, (
				f"{UFW} allow from {other_ip}"
				for other_ip in previous_instance_ips.union(new_instance_ips)
			), threads)
		for previous_ip in previous_instance_ips:
			threads.append(
				extend_network(previous_ip, new_instance_ips, True)
			)
		for new_ip in new_instance_ips:
			threads.append(
				extend_network(
					new_ip,
					previous_instance_ips.union(new_instance_ips),
					True,
				)
			)
		for new_instance in new_instances:
			threads.append(
				set_region_and_public_ipv4(
					new_instance.main_ip,
					new_instance.region,
					new_instance.main_ip,
				)
			)
		wait_then_clear(threads)
		# Run each worker.
		for new_ip in new_instance_ips:
			if new_ip == main_ip:
				threads.append(StartMainWorker.run_on_host(new_ip))
			else:
				threads.append(StartWorker.run_on_host(new_ip))
		wait_then_clear(threads)
