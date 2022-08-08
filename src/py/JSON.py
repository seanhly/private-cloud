from json import dump, dumps, load, loads, JSONEncoder
from typing import Any


class SetEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, set):
			return list(obj)
		return JSONEncoder.default(self, obj)


INDENTED_DUMP_ARGS = dict(
	separators=(", ", ": "),
	sort_keys=True,
	indent="\t",
	cls=SetEncoder,
)
COMPACT_DUMP_ARGS = dict(
	separators=(",", ":"),
	sort_keys=True,
	indent=None,
	cls=SetEncoder,
)


class JSON:
	@classmethod
	def dumps(cls, obj: Any, indent: bool = True):
		if indent:
			return dumps(obj, **INDENTED_DUMP_ARGS)
		return dumps(obj, **COMPACT_DUMP_ARGS)

	@classmethod
	def dump(cls, obj: Any, fp, indent: bool = True):
		if indent:
			return dump(obj, fp, **INDENTED_DUMP_ARGS)
		return dump(obj, fp, **COMPACT_DUMP_ARGS)

	@classmethod
	def loads(cls, content: str):
		return loads(content)

	@classmethod
	def load(cls, fp):
		return load(fp)
