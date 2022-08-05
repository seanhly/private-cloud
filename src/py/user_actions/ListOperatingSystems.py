from user_actions.UserAction import UserAction
from cloud.vendors.Vultr import Vultr


class ListOperatingSystems(UserAction):
	@classmethod
	def command(cls) -> str:
		return "ls-os"

	@classmethod
	def description(cls):
		return "List available cloud operating systems"

	def execute(self) -> None:
		for os in Vultr.list_operating_systems():
			print(str(os))
