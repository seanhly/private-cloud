from user_actions.UserAction import UserAction
from cloud.server.Pool import Pool
from cloud.vendors.Vultr import Vultr
from constants import (
	CRYPTPAD_BACKUP_DIR, CRYPTPAD_USER_DIR, CRYPTPAD_USER,
)
from util.rsync import rsync
from os.path import exists
from os import makedirs


class RestoreCryptpad(UserAction):
	@classmethod
	def command(cls) -> str:
		return "restore"

	@classmethod
	def description(cls):
		return "Restore Cryptpad data."

	def execute(self) -> None:
		vendor = Vultr
		instances = vendor.list_instances()
		Pool.load(vendor).update(instances)
		if not exists(CRYPTPAD_BACKUP_DIR):
			makedirs(CRYPTPAD_BACKUP_DIR)
		for i in instances:
			rsync(
				CRYPTPAD_BACKUP_DIR,
				CRYPTPAD_USER_DIR,
				host=i.main_ip,
				user=CRYPTPAD_USER,
				chmod=0o777
			)
