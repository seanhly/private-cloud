from user_actions.UserAction import UserAction
from cloud.vendors.Vultr import Vultr


class RebootInstance(UserAction):
	@classmethod
	def command(cls) -> str:
		return "reboot"

	@classmethod
	def description(cls):
		return "Reboot a server instance"

	def execute(self) -> None:
		vendor = Vultr
		q = self.query.strip()
		print(vendor.reboot(q))
