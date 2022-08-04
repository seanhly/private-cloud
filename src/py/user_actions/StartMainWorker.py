from constants import CRYPTPAD_DIR_PATH, CRYPTPAD_SOURCE, CRYPTPAD_USER
from os.path import basename
from user_actions.StartWorker import StartWorker


class StartMainWorker(StartWorker):
	@classmethod
	def command(cls) -> str:
		return "start-main"

	@classmethod
	def description(cls):
		return "Start main worker node."

	def special_services(self):
		return {
			basename(CRYPTPAD_SOURCE): (
				CRYPTPAD_DIR_PATH,
				CRYPTPAD_USER,
				"node server.js"
			)
		}