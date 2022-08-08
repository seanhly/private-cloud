from json import dump, dumps, load, loads, JSONEncoder
from typing import Any


class SetEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, set):
			return list(obj)
		return JSONEncoder.default(self, obj)


DUMP_ARGS = dict(
	separators=(",", ":"),
	sort_keys=True,
	indent="\t",
	cls=SetEncoder,
)


class JSON:
	@classmethod
	def dumps(cls, obj: Any):
		return dumps(obj, **DUMP_ARGS)

	@classmethod
	def dump(cls, obj: Any, fp):
		return dump(obj, fp, **DUMP_ARGS)

	@classmethod
	def loads(cls, content: str):
		return loads(content)

	@classmethod
	def load(cls, fp):
		return load(fp)
