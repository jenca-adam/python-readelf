from readelf.helpers import endian_read
from readelf.const import ARCH


def parse_sec_offset(stream, meta, supp, cu):
    addr_size = 8 if meta.arch == ARCH.ARCH_64 else 4
    return endian_read(stream, meta.endian, addr_size)
