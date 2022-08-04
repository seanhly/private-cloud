from abc import ABC, abstractmethod
from typing import List, Optional

from cloud.server.Instance import Instance


class Vendor(ABC):
	@classmethod
	@abstractmethod
	def list_plans(cls):
		pass

	@classmethod
	@abstractmethod
	def list_regions(cls):
		pass

	@classmethod
	@abstractmethod
	def list_operating_systems(cls):
		pass

	@classmethod
	@abstractmethod
	def list_ssh_keys(cls):
		pass

	@classmethod
	@abstractmethod
	def list_instances(cls, label: Optional[str] = None) -> List[Instance]:
		pass

	@classmethod
	@abstractmethod
	def get_instance(cls, the_id: str) -> Instance:
		pass

	@classmethod
	@abstractmethod
	def create_instance(cls, region, plan, os, sshkey):
		pass

	@classmethod
	@abstractmethod
	def destroy_instance(cls, the_id: str):
		pass
