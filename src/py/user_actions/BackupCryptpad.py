from user_actions.UserAction import UserAction
from cloud.server.Pool import Pool
from cloud.vendors.Vultr import Vultr
from constants import CRYPTPAD_BACKUP_DIR, BACKUP_CRYPTPAD_DIRS
from util.rsync import rsync
from os.path import exists
from os import makedirs


class BackupCryptpad(UserAction):
	@classmethod
	def command(cls) -> str:
		return "backup"

	@classmethod
	def description(cls):
		return "Backup Cryptpad data."

	def execute(self) -> None:
		vendor = Vultr
		instances = vendor.list_instances()
		Pool.load(vendor).update(instances)
		if not exists(CRYPTPAD_BACKUP_DIR):
			makedirs(CRYPTPAD_BACKUP_DIR)
		for i in instances:
			rsync(
				BACKUP_CRYPTPAD_DIRS,
				CRYPTPAD_BACKUP_DIR,
				host=i.main_ip,
				reverse=True,
				delete_extraneous_files=True,
			)
