from user_actions.UserAction import UserAction
from cloud.vendors.Vultr import Vultr


class ListSSHKeys(UserAction):
	@classmethod
	def command(cls) -> str:
		return "ls-ssh"

	@classmethod
	def description(cls):
		return "List available SSH keys"

	def execute(self) -> None:
		for ssh in Vultr.list_ssh_keys():
			print(str(ssh))
