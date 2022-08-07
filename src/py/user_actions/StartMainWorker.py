from constants import (
	CRYPTPAD_DIR_PATH, CRYPTPAD_SOURCE, CRYPTPAD_USER, GIT_USER,
	GIT_USER_HOME_DIR, NODE, GIT
)
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
				f"{NODE} server.js"
			),
			GIT_USER: (
				GIT_USER_HOME_DIR,
				GIT_USER,
				" ".join([
					GIT,
					"daemon",
					"--base-path=.",
					"--export-all",
					"--reuseaddr",
					"--informative-errors",
					"--verbose",
				])
			)
		}
