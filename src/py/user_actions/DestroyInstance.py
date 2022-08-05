from user_actions.UserAction import UserAction
from cloud.vendors.Vultr import Vultr
from cloud.server.Pool import Pool
from constants import PROJECT_LABEL


class DestroyInstance(UserAction):
	@classmethod
	def command(cls) -> str:
		return "rm"

	@classmethod
	def description(cls):
		return "Destroy a server instance"
	
	def execute(self) -> None:
		q = self.query.strip()
		current_pool = Pool.load(Vultr)
		for instance in Vultr.list_instances(label=PROJECT_LABEL):
			if (
				instance.main_ip == q
				or instance.id == q
			):
				instance.destroy()
				current_pool.remove(instance.id)
		current_pool.dump()
