from subprocess import Popen
from typing import List
from user_actions.UserAction import UserAction
from cloud.server.Pool import Pool
from cloud.vendors.Vultr import Vultr
from constants import EXECUTABLE, LOCAL_EXECUTABLE
from util.scp import scp
from util.wait_then_clear import wait_then_clear


class UpdateAll(UserAction):
	@classmethod
	def command(cls) -> str:
		return "u"

	@classmethod
	def description(cls):
		return "Update all the deployed instances"

	def execute(self) -> None:
		vendor = Vultr
		instances = vendor.list_instances()
		Pool.load(vendor).update(instances)
		threads: List[Popen] = []
		for i in instances:
			threads.append(scp(LOCAL_EXECUTABLE, i.main_ip, EXECUTABLE))
		wait_then_clear(threads)
