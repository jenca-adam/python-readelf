from ..err import ParseError
from ..const import *
from ..maps import *
from ..helpers import endian_read

ET_LOOS = 0xFE00
ET_HIOS = 0xFEFF
ET_LOPROC = 0xFF00
ET_HIPROC = 0xFFFF

RESERVED_ISA_RANGES = (range(0x18, 0x23), range(0x0B, 0x0D))


def parse_header(buf):
    output = {}

    magic = buf.read(4)
    if magic != b"\x7fELF":
        raise ParseError(f"Wrong magic number {magic!r}!")

    arch = ord(buf.read(1))
    if arch not in (1, 2):
        raise ParseError(f"Invalid EI_CLASS {arch}!")
    output["arch"] =arch= ARCH_MAP[arch]
    ADDR_SIZE=4 if arch==ARCH_32 else 8

    endian = ord(buf.read(1))
    if endian not in (1, 2):
        raise ParseError(f"Invalid EI_DATA {endian}!")
    output["endian"] = endian = ENDIAN_MAP[endian]

    version = ord(buf.read(1))
    if version != 1:
        raise ParseError(f"EI_VER should be 1, got {version}")
    output["version"] = EI_VER_1

    abi = ord(buf.read(1))
    if abi not in ABI_MAP:
        raise ParseError(f"Invalid EI_OSABI {hex(abi)}!")
    output["abi"] = ABI_MAP[abi]

    buf.read(8)  # ignore ABI_VERSION for now

    et = endian_read(buf, endian, 2)
    if et in ET_MAP:
        e_type = ET_MAP[et]
    elif ET_LOOS <= et <= ET_HIOS:
        e_type = ET_OS
    elif ET_LOPROC <= et <= ET_HIPROC:
        e_type = ET_PROC
    else:
        raise ParseError(f"Invalid e_type {hex(et)}")
    output["e_type"] = e_type

    isa_int = endian_read(buf, endian, 2)

    if isa_int in ISA_MAP:
        isa = ISA_MAP[isa_int]
    else:
        for rng in RESERVED_ISA_RANGES:
            if isa_int in rng:
                isa = ISA_RESERVED
        else:
            raise ParseError(f"Unknown ISA {hex(isa_int)}")
    output["isa"] = isa
    
    e_version = endian_read(buf,endian,4)
    if e_version!=1:
        raise ParseError(f"e_version should be 1, got {e_version}")
    output["e_version"] = e_version

    entry_point = endian_read(buf,endian,ADDR_SIZE)
    output["entry_point"]=entry_point
    
    phoff = endian_read(buf,endian,ADDR_SIZE)
    output["program_header_start"]=phoff

    shoff = endian_read(buf,endian,ADDR_SIZE)
    output["section_header_start"]=shoff

    flags =  endian_read(buf,endian,4)
    output["flags"]=flags

    header_size = endian_read(buf,endian,2)
    output["header_size"]=header_size
    
    ph_size = endian_read(buf,endian,2)
    output["program_header_size"]=ph_size

    ph_num = endian_read(buf,endian,2)
    output["program_header_entries"]=ph_num

    sh_size = endian_read(buf,endian,2)
    output["section_header_size"]=sh_size

    sh_num = endian_read(buf,endian,2)
    output["section_header_entries"]=ph_num

    sh_strndx = endian_read(buf,endian,2)
    output["section_header_names_index"]=sh_strndx
    
    return output
