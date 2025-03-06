from readelf.dwarf.leb128 import leb128_parse


def parse_exprloc(stream, cu, supp):
    length = leb128_parse(stream)
    return stream.read(length)
