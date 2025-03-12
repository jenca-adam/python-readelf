from readelf.dwarf.leb128 import leb128_parse
from readelf.helpers import endian_read

def parse_data1(stream, cu, supp):
    return endian_read(stream, cu.parent.elf_file.endian, 1)


def parse_data2(stream, cu, supp):
    return endian_read(stream, cu.parent.elf_file.endian, 2)


def parse_data4(stream, cu, supp):
    return endian_read(stream, cu.parent.elf_file.endian, 4)


def parse_data8(stream, cu, supp):
    return endian_read(stream, cu.parent.elf_file.endian, 8)


def parse_udata(stream, cu, supp):
    return leb128_parse(stream, signed=False)


def parse_sdata(stream, cu, supp):
    return leb128_parse(stream, signed=True)


def parse_implicit_const(stream, cu, supp):
    return supp
