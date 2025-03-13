from readelf.helpers import endian_read


def parse_addr(stream, meta, supp):
    return endian_read(stream, meta.endian, meta.addr_size)


# TODO addr tab
