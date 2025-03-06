def parse_string(stream, cu, supp):
    outp = []
    while True:
        c = stream.read(1)
        if not c or c==b'\x00':
            break
        outp.append(ord(c))
    return bytes(outp)
    
