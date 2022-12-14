from genericpath import exists
from cloud.vendors.Vultr import Vultr
from constants import (
	PROJECT_PRIVATE_RSA_KEY, PROJECT_PUBLIC_RSA_KEY, USER, PROJECT_LABEL,
	SSH_KEYGEN_BINARY, HOSTNAME_FILE
)
import subprocess


class SSHKeys:
	@classmethod
	def default_ssh_key(cls):
		with open(HOSTNAME_FILE, "r") as f:
			hostname = f.read().strip()
		name = f"{PROJECT_LABEL}_{hostname}_{USER}"
		if exists(PROJECT_PUBLIC_RSA_KEY):
			with open(PROJECT_PUBLIC_RSA_KEY, "r") as f:
				local_ssh = f.read().strip()
			remote_ssh_key = None
			remote_keys = Vultr.list_ssh_keys()
			i = 0
			while i < len(remote_keys) and not remote_ssh_key:
				ssh_key = remote_keys[i]
				if ssh_key.name == name:
					remote_ssh_key = ssh_key
					if ssh_key.ssh_key.strip() == local_ssh:
						return ssh_key
				i += 1
		else:
			remote_ssh_key = None
			subprocess.Popen(
				[SSH_KEYGEN_BINARY, "-P", "", "-f", PROJECT_PRIVATE_RSA_KEY]
			).wait()
			with open(PROJECT_PUBLIC_RSA_KEY, "r") as f:
				local_ssh = f.read().strip()
		if remote_ssh_key:
			Vultr.patch_ssh_key(remote_ssh_key.id, name, local_ssh)
			return remote_ssh_key
		else:
			return Vultr.create_ssh_key(name, local_ssh)
