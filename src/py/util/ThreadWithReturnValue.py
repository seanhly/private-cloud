from threading import Thread
from typing import Any


class ThreadWithReturnValue(Thread):
	def __init__(
		self, group=None, target=None, name=None, args=(), kwargs=None,
	):
		if not kwargs:
			kwargs = {}
		Thread.__init__(self, group, target, name, args, kwargs)
		self._return = None

	def run(self):
		self: Any
		if self._Thread__target is not None:
			self._return = self._Thread__target(
				*self._Thread__args,
				**self._Thread__kwargs,
			)

	def join(self) -> bool:
		Thread.join(self)
		return self._return
