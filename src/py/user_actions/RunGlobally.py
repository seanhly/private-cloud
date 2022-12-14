from subprocess import Popen
from typing import List
from user_actions.UserAction import UserAction
from cloud.server.Pool import Pool
from cloud.vendors.Vultr import Vultr
from util.ssh_do import ssh_do
from re import sub


class RunGlobally(UserAction):
	@classmethod
	def command(cls) -> str:
		return "do"

	@classmethod
	def description(cls):
		return "Run a command on all worker machines simultaneously."

	def execute(self) -> None:
		vendor = Vultr
		instances = vendor.list_instances()
		Pool.load(vendor).update(instances)
		threads: List[Popen] = []
		cmd = self.query.strip()
		cmd = sub("^[\"']", "", cmd)
		cmd = sub("[\"']$", "", cmd)
		for i in instances:
			ssh_do(i.main_ip, cmd, threads)
		for thread in threads:
			thread.wait()
