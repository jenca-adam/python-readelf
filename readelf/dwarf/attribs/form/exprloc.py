from readelf.dwarf.leb128 import leb128_parse
from readelf.dwarf.expression import Expression
from io import BytesIO


def parse_exprloc(stream, meta, supp, cu):
    length = leb128_parse(stream)
    return Expression.parse(BytesIO(stream.read(length)), cu, meta)
