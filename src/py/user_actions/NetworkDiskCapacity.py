from typing import Dict, Set
from user_actions.UserAction import UserAction
from cloud.vendors.Vultr import Vultr
from util.ssh_do import ssh_do


class NetworkDiskCapacity(UserAction):
	@classmethod
	def command(cls) -> str:
		return "ndc"

	@classmethod
	def description(cls):
		return "Print information about the network disk capacity"

	def execute(self) -> None:
		vendor = Vultr
		instances = vendor.list_instances()
		instance_ips: Set[str] = set(
			i.main_ip for i in instances
		)
		right_of: Dict[str, str] = {}
		for ip in instance_ips:
			r = (
				ssh_do(
					ip,
					"/usr/bin/redis-cli",
					None,
					"mget R",
					stdout=True,
				)
					.stdout
					.read()
					.decode()
					.strip()
			)
			right_of[ip] = r
		first_ip = [i for i in instance_ips][0]
		next_ip = right_of[first_ip]
		ordered_ips = [first_ip]
		while next_ip != first_ip:
			ordered_ips.append(next_ip)
			next_ip = right_of[next_ip]
		total_available = 0
		for ip in ordered_ips:
			available = int(
				ssh_do(
					ip,
					"/usr/bin/df -B1 /",
					stdout=True,
				)
					.stdout
					.read()
					.decode()
					.strip()
					.split("\n")[-1]
					.split()[3]
			)
			print(f"%.2f GB ({ip})" % (available / ((2 ** 10) ** 3)))
			total_available += available
		print("----------------------")
		print("\t%.2f GB (total)" % (total_available / ((2 ** 10) ** 3)))
