from .const import *

def endian_read(buf,endian,n):
    if endian==ENDIAN_BIG:
        e="big"
    elif endian==ENDIAN_LITTLE:
        e="little"
    else:
        raise ValueError("Bad endian")
    return int.from_bytes(buf.read(n),e)
