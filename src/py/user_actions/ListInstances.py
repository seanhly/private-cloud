from user_actions.UserAction import UserAction
from cloud.server.Pool import Pool
from cloud.vendors.Vultr import Vultr


class ListInstances(UserAction):
	@classmethod
	def command(cls) -> str:
		return "ls"

	@classmethod
	def description(cls):
		return "List server instances"

	def execute(self) -> None:
		vendor = Vultr
		instances = vendor.list_instances()
		Pool.load(vendor).update(instances)
		for i in instances:
			print(str(i))
