from readelf.dwarf.leb128 import leb128_parse


def parse_data1(stream, cu, supp):
    return stream.read(1)


def parse_data2(stream, cu, supp):
    return stream.read(2)


def parse_data4(stream, cu, supp):
    return stream.read(4)


def parse_data8(stream, cu, supp):
    return stream.read(8)


def parse_udata(stream, cu, supp):
    return leb128_parse(stream, signed=False)


def parse_sdata(stream, cu, supp):
    return leb128_parse(stream, signed=True)


def parse_implicit_const(stream, cu, supp):
    return supp
