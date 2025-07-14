from readelf.dwarf.leb128 import leb128_parse
from readelf.helpers import endian_read


def parse_data1(stream, meta, supp, cu):
    return endian_read(stream, meta.endian, 1)


def parse_data2(stream, meta, supp, cu):
    return endian_read(stream, meta.endian, 2)


def parse_data4(stream, meta, supp, cu):
    return endian_read(stream, meta.endian, 4)


def parse_data8(stream, meta, supp, cu):
    return endian_read(stream, meta.endian, 8)


def parse_udata(stream, meta, supp, cu):
    return leb128_parse(stream, signed=False)


def parse_sdata(stream, meta, supp, cu):
    return leb128_parse(stream, signed=True)


def parse_implicit_const(stream, meta, supp, cu):
    return supp
