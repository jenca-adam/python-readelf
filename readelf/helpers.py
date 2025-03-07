from .const import *
import math
import struct

def is_eof(bytes_io):
    return bytes_io.tell() == len(bytes_io.getbuffer())


def extract_sections(
    elf_file, *sec_names, required=None, errmsg="missing section: {!r}"
):
    secs = []
    for i, sn in enumerate(sec_names):
        try:
            secs.append(elf_file.find_section(sn))
        except LookupError:
            if required is not None and i in required:
                raise LookupError(errmsg.format(sn)) from None
            else:
                secs.append(None)
    return secs


def endian_read(buf, endian, n, **kwargs):
    read_result = buf.read(n)
    if len(read_result) < n:
        raise EOFError("eof while reading integer")
    return endian_parse(read_result, endian, **kwargs)


def endian_parse(data, endian, **kwargs):
    if endian == ENDIAN.ENDIAN_BIG:
        e = "big"
    elif endian == ENDIAN.ENDIAN_LITTLE:
        e = "little"
    else:
        raise ValueError(f"Bad endian: {endian}")
    return int.from_bytes(data, e, **kwargs)


def read_struct(stream, fmt, endian=None):
    if endian:
        endian_char = {ENDIAN.ENDIAN_LITTLE: "<", ENDIAN.ENDIAN_BIG: ">"}.get(
            endian, ""
        )
        fmt = endian_char + fmt
    sz = struct.calcsize(fmt)
    b = stream.read(sz)
    return struct.unpack(fmt, b)


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
