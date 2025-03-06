from readelf.helpers import endian_read
from readelf.const import ARCH


def parse_sec_offset(stream, cu, supp):
    size = 4 if cu.arch == ARCH.ARCH_32 else 8
    return endian_read(stream, cu.parent.elf_file.endian, size)
