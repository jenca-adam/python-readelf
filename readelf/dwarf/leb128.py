def leb128_parse(stream, signed=False):
    out = 0
    shift = 0

    while True:
        byte = stream.read(1)
        if not byte:
            raise EOFError("MSB set on last byte of input")
        value = byte[0]
        out |= (value & 0x7F) << shift
        shift += 7
        if not (value & 0x80):
            break
    if signed and (value & 0x40):
        out |= ~0 << shift
    return out


def leb128_encode(i, signed=False):
    barr = bytearray()
    while True:
        i, j = i >> 7, i & 0x7F
        if (
            signed
            and ((i == 0 and not j & 0x40) or (i == -1 and j & 0x40))
            or not signed
            and not i
        ):
            barr.append(j)
            break
        else:
            barr.append(j | 0x80)
    return barr
