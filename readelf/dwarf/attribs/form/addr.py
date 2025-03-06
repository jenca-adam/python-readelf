from readelf.helpers import endian_read

def parse_addr(stream, cu, supp):
    return endian_read(stream, cu.parent.elf_file.endian, cu.addr_size)

# TODO addr tab
