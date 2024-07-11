from .const import *
import math


def endian_read(buf, endian, n, **kwargs):
    return endian_parse(buf.read(n), endian, **kwargs)


def endian_parse(data, endian, **kwargs):
    if endian == ENDIAN.ENDIAN_BIG:
        e = "big"
    elif endian == ENDIAN.ENDIAN_LITTLE:
        e = "little"
    else:
        raise ValueError("Bad endian")
    return int.from_bytes(data, e, **kwargs)


def split_array(data, chunk_size, endian):
    return [
        endian_parse(data[i : i + chunk_size], endian)
        for i in range(0, len(data), chunk_size)
    ]


def map_public_attributes(src, dest):
    for name in dir(src):
        if name.startswith("__"):  # don't copy dunders over
            continue

        dest.__setattr__(name, getattr(src, name))
