import subprocess
from typing import List, Optional, Set, Type, cast
from JSON import JSON
from cloud.Vendor import Vendor
from cloud.server.Instance import Instance
from cloud.server.OperatingSystem import OperatingSystem
from cloud.server.Plan import Plan
from cloud.server.Region import Region
from cloud.server.SSHKey import SSHKey
from cloud.server.Entity import Entity
import re
from constants import VULTR_TOKEN, PROJECT_LABEL


def lowest_cost_per_disk(plan: Plan):
	return (plan.disk * plan.disk_count) / plan.monthly_cost


def os_family_name_then_version(os: OperatingSystem):
	key = [os.family, *(os.name.split())]
	if len(key) >= 3:
		if re.fullmatch("[0-9]+(\\.[0-9]+)?", key[2]):
			key[2] = -float(key[2])
		else:
			key.insert(2, 9e99)
	return tuple(key)


def plural(singular: str):
	if len(singular) <= 2 and singular[-1] == "s":
		return singular
	return f"{singular}s"


class Vultr(Vendor):
	@classmethod
	def get(cls, entity: Type[Entity], label: str, the_id: str = None):
		if the_id:
			suffix = f"/{the_id}"
			result_key = label
		else:
			suffix = "?per_page=500"
			result_key = plural(label)
		from requests import get
		loaded_json = JSON.loads(
			get(f"https://api.vultr.com/v2/{plural(label)}{suffix}", headers={
				"Authorization": f"Bearer {VULTR_TOKEN}",
			}).content.decode()
		)
		inner_json = loaded_json[result_key.replace("-", "_")]
		if the_id:
			return entity(inner_json, cls)
		else:
			return (entity(inner, cls) for inner in inner_json)

	@classmethod
	def reboot(cls, the_id: str = None):
		from requests import post
		return post(
			f"https://api.vultr.com/v2/instances/{the_id}/reboot",
			headers={"Authorization": f"Bearer {VULTR_TOKEN}"}
		).content.decode()

	@classmethod
	def list_regions(cls):
		return list(cls.get(Region, "region"))

	@classmethod
	def list_plans(
			cls,
			min_ram=0,
			max_cost=9e99,
			sort_by=lowest_cost_per_disk,
			region: Region = None
	):
		plans = [
			plan
			for plan in cls.get(Plan, "plan")
			if (
					plan.monthly_cost <= max_cost
					and plan.ram >= min_ram
					and (not region or region.id in plan.locations)
			)
		]
		plans.sort(key=sort_by)

		return plans

	@classmethod
	def list_operating_systems(
			cls,
			os_family: Optional[str] = None,
			sort_by=os_family_name_then_version,
			in_name: Set[str] = None,
	):
		if not in_name:
			in_name = set()
		operating_systems = [
			os
			for os in cls.get(OperatingSystem, "os")
			if (
					(not os_family or os.family == os_family)
					and all(substring in os.name for substring in in_name)
			)
		]
		operating_systems.sort(key=sort_by)

		return operating_systems

	@classmethod
	def list_ssh_keys(cls) -> List[SSHKey]:
		return list(cls.get(SSHKey, "ssh-key"))

	@classmethod
	def list_instances(
		cls, label: Optional[str] = PROJECT_LABEL
	) -> List[Instance]:
		return [
			i
			for i in cls.get(Instance, "instance")
			if (not label or label == i.label)
		]

	@classmethod
	def get_instance(cls, the_id: str) -> Instance:
		instance = cast(Instance, cls.get(Instance, "instance", the_id))
		return instance

	@classmethod
	def create_instance(
			cls,
			region: Region = None,
			plan: Plan = None,
			os: OperatingSystem = None,
			sshkey: SSHKey = None,
			**kwargs
	):
		if not region:
			from cloud.server.Regions import Regions
			region = Regions.nearest_region()
		if not plan:
			from cloud.server.Plans import Plans
			plan = Plans.cheapest_plan(region=region, **kwargs)
		if not os:
			from cloud.server.OperatingSystems import OperatingSystems
			os = OperatingSystems.default_os()
		if not sshkey:
			from cloud.server.SSHKeys import SSHKeys
			sshkey = SSHKeys.default_ssh_key()
		return Instance(
			JSON.loads(subprocess.check_output(
				[
					"/usr/bin/curl",
					'https://api.vultr.com/v2/instances',
					"-X",
					"POST",
					"-H",
					f"Authorization: Bearer {VULTR_TOKEN}",
					"-H",
					"Content-Type: application/json",
					"--data",
					JSON.dumps(
						dict(
							region=region.id,
							plan=plan.id,
							label=PROJECT_LABEL,
							os_id=os.id,
							backups="disabled",
							sshkey_id=[sshkey.id],
							enable_ipv6=True,
							activation_email=False,
							enable_vpc=True,
						)
					),
				],
				stderr=subprocess.DEVNULL
			).decode())["instance"],
			vendor=cls,
		)

	@classmethod
	def create_ssh_key(cls, name: str, ssh_key: str):
		return SSHKey(
			JSON.loads(subprocess.check_output(
				[
					"/usr/bin/curl",
					'https://api.vultr.com/v2/ssh-keys',
					"-X",
					"POST",
					"-H",
					f"Authorization: Bearer {VULTR_TOKEN}",
					"-H",
					"Content-Type: application/json",
					"--data",
					JSON.dumps(dict(name=name, ssh_key=ssh_key)),
				],
				stderr=subprocess.DEVNULL
			).decode())["ssh_key"],
			vendor=cls,
		)

	@classmethod
	def patch_ssh_key(cls, the_id: str, name: str, ssh_key: str):
		subprocess.Popen(
			[
				"/usr/bin/curl",
				f"https://api.vultr.com/v2/ssh-keys/{the_id}",
				"-X",
				"PATCH",
				"-H",
				f"Authorization: Bearer {VULTR_TOKEN}",
				"-H",
				"Content-Type: application/json",
				"--data",
				JSON.dumps(dict(name=name, ssh_key=ssh_key)),
			],
			stderr=subprocess.DEVNULL
		).wait()

	@classmethod
	def destroy_instance(cls, the_id: str):
		print(subprocess.check_output(
			[
				"/usr/bin/curl",
				f"https://api.vultr.com/v2/instances/{the_id}",
				"-X",
				"DELETE",
				"-H",
				f"Authorization: Bearer {VULTR_TOKEN}",
			],
			stderr=subprocess.DEVNULL
		).decode())
