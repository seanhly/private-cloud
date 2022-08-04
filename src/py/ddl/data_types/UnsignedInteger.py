from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import INTEGER

UnsignedInteger = Integer()
UnsignedInteger = UnsignedInteger.with_variant(
	INTEGER(unsigned=True),
	'postgresql'
)