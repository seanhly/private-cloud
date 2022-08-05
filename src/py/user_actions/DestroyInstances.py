from user_actions.UserAction import UserAction
from cloud.vendors.Vultr import Vultr
from cloud.server.Pool import Pool
from constants import PROJECT_LABEL


class DestroyInstances(UserAction):
	@classmethod
	def command(cls) -> str:
		return "rma"

	@classmethod
	def description(cls):
		return "Destroy all server instances"
	
	def execute(self) -> None:
		current_pool = Pool.load(Vultr)
		for instance in Vultr.list_instances(label=PROJECT_LABEL):
			instance.destroy()
			current_pool.remove(instance.id)
		current_pool.dump()
