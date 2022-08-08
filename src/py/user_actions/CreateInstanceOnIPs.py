from JSON import JSON
from subprocess import Popen
from user_actions.UserAction import UserAction
from cloud.server.Pool import Pool
from cloud.vendors.Vultr import Vultr
from typing import List
from constants import BOOTSTRAP_SCRIPT
from util.ssh_do import ssh_do
from util.redis_utils import extend_network


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
		# Pre-existing workers can now reach new workers.
		extend_network(previous_instance_ips, new_instance_ips)
		threads: List[Popen] = []
		# Bootstrap a system onto each worker.
		for new_instance in new_instances:
			new_ip = new_instance.main_ip
			ip = new_instance.main_ip
			input_data = dict(
				public_ipv4=new_instance.main_ip,
				region=new_instance.region,
				network=(
					previous_instance_ips
						.union(new_instance_ips)
						.difference({ip})
				),
				is_main=(new_ip == main_ip),
			)
			if certbot_suffix:
				input_data[CERTBOT_SUFFIX_OPTION] = certbot_suffix
			threads.append(
				ssh_do(new_ip, BOOTSTRAP_SCRIPT, stdin=JSON.dumps(input_data))
			)