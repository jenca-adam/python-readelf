from .const import *


def endian_read(buf, endian, n):
    if endian == ENDIAN_BIG:
        e = "big"
    elif endian == ENDIAN_LITTLE:
        e = "little"
    else:
        raise ValueError("Bad endian")
    return int.from_bytes(buf.read(n), e)


def map_public_attributes(src, dest):
    for name in dir(src):
        if name.startswith("__"):  # don't copy dunders over except __repr__
            continue

        dest.__setattr__(name, getattr(src, name))
