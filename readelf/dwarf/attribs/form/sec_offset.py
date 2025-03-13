from readelf.helpers import endian_read
from readelf.const import ARCH


def parse_sec_offset(stream, meta, supp):
    return endian_read(stream, meta.endian, meta.addr_size)
