from sqlalchemy import SmallInteger
from sqlalchemy.dialects.postgresql import SMALLINT

UnsignedSmallInteger = SmallInteger()
UnsignedSmallInteger = UnsignedSmallInteger.with_variant(
	SMALLINT(unsigned=True),
	'postgresql'
)