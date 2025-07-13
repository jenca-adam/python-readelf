from .err import ParseError
from .const import *
from .maps import *
from .helpers import endian_read
import math

ET_LOOS = 0xFE00
ET_HIOS = 0xFEFF
ET_LOPROC = 0xFF00
ET_HIPROC = 0xFFFF

PT_LOOS = 0x60000000
PT_HIOS = 0x6FFFFFFF
PT_LOPROC = 0x70000000
PT_HIPROC = 0x7FFFFFFF

SHT_LOOS = 0x60000000
RESERVED_ISA_RANGES = (range(0x18, 0x23), range(0x0B, 0x0D))


def parse_header(buf):
    output = {}

    magic = buf.read(4)
    if magic != b"\x7fELF":
        raise ParseError(f"Wrong magic number {magic!r}!")

    arch = ord(buf.read(1))
    if arch not in (1, 2):
        raise ParseError(f"Invalid EI_CLASS {arch}!")
    output["arch"] = arch = ARCH(arch)
    ADDR_SIZE = 4 if arch == ARCH.ARCH_32 else 8

    endian = ord(buf.read(1))
    if endian not in (1, 2):
        raise ParseError(f"Invalid EI_DATA {endian}!")
    output["endian"] = endian = ENDIAN(endian)

    version = ord(buf.read(1))

    if version != 1:
        raise ParseError(f"EI_VER should be 1, got {version}")
    output["version"] = EI_VER(version)

    abi = ord(buf.read(1))
    if abi not in ABI:
        raise ParseError(f"Invalid EI_OSABI {hex(abi)}!")
    output["abi"] = ABI(abi)

    buf.read(8)  # ignore ABI_VERSION for now

    et = endian_read(buf, endian, 2)
    if et in ET:
        e_type = ET(et)
    elif ET_LOOS <= et <= ET_HIOS:
        e_type = ET.ET_OS
    elif ET_LOPROC <= et <= ET_HIPROC:
        e_type = ET.ET_PROC
    else:
        raise ParseError(f"Invalid e_type {hex(et)}")
    output["type"] = e_type
    output["type_int"] = et

    isa_int = endian_read(buf, endian, 2)

    if isa_int in ISA:
        isa = ISA(isa_int)
    else:
        for rng in RESERVED_ISA_RANGES:
            if isa_int in rng:
                isa = ISA.ISA_RESERVED
        else:
            raise ParseError(f"Unknown ISA {hex(isa_int)}")
    output["isa"] = isa

    e_version = endian_read(buf, endian, 4)
    if e_version != 1:
        raise ParseError(f"e_version should be 1, got {e_version}")

    entry_point = endian_read(buf, endian, ADDR_SIZE)
    output["entry"] = entry_point

    phoff = endian_read(buf, endian, ADDR_SIZE)
    output["phoff"] = phoff

    shoff = endian_read(buf, endian, ADDR_SIZE)
    output["shoff"] = shoff

    flags = endian_read(buf, endian, 4)
    output["flags"] = flags

    header_size = endian_read(buf, endian, 2)
    output["ehsize"] = header_size

    ph_size = endian_read(buf, endian, 2)
    output["phentsize"] = ph_size

    ph_num = endian_read(buf, endian, 2)
    output["phnum"] = ph_num

    sh_size = endian_read(buf, endian, 2)
    output["shentsize"] = sh_size

    sh_num = endian_read(buf, endian, 2)
    output["shnum"] = sh_num

    sh_strndx = endian_read(buf, endian, 2)
    output["shstrndx"] = sh_strndx
    return output


def parse_program_header(buf, phoff, ph_size, ph_num, endian, arch):
    ADDR_SIZE = 4 if arch == ARCH.ARCH_32 else 8
    buf.seek(phoff)

    segm = []

    for _ in range(ph_num):
        r = {}

        p_type_int = endian_read(buf, endian, 4)
        if PT_LOOS <= p_type_int <= PT_HIOS:
            p_type = PT.PT_OS
        elif PT_LOPROC <= p_type_int <= PT_HIPROC:
            p_type = PT.PT_PROC
        elif p_type_int not in PT:
            raise ParseError(f"invalid p_type {hex(p_type)}")
        else:
            p_type = PT(p_type_int)
        r["type"] = p_type
        if arch == ARCH.ARCH_64:
            r["flags"] = endian_read(buf, endian, 4)
        r["offset"] = offset = endian_read(buf, endian, ADDR_SIZE)
        r["vaddr"] = vaddr = endian_read(buf, endian, ADDR_SIZE)
        r["paddr"] = endian_read(buf, endian, ADDR_SIZE)  # irrelevant
        r["filesz"] = endian_read(buf, endian, ADDR_SIZE)
        r["memsz"] = endian_read(buf, endian, ADDR_SIZE)
        if arch == ARCH.ARCH_32:
            r["flags"] = endian_read(buf, endian, 4)
        align = endian_read(buf, endian, ADDR_SIZE)
        if align > 1:
            if math.log(align, 2) % 1 != 0:
                raise ParseError("Wrong p_align: should be 0 or power of 2.")
            if vaddr % align != offset % align:
                raise ParseError(
                    "Wrong p_align: p_offset mod p_align != p_vaddr mod p_align"
                )
        r["align"] = align
        segm.append(r)
        buf.read(ph_size - (6 * ADDR_SIZE + 8))  # ignore the rest
    return segm


def parse_section_header(buf, shoff, sh_size, sh_num, endian, arch):
    ADDR_SIZE = 4 if arch == ARCH.ARCH_32 else 8
    buf.seek(shoff)
    sections = []

    for _ in range(sh_num):
        s = {}
        s["name"] = endian_read(buf, endian, 4)
        sh_type = endian_read(buf, endian, 4)
        if sh_type > SHT_LOOS:
            s["type"] = SHT.SHT_OS
        elif sh_type not in SHT:
            raise ParseError(f"invalid sh_type: {sh_type:#x}")
        else:
            s["type"] = SHT(sh_type)
        sh_flags = endian_read(buf, endian, ADDR_SIZE)
        f = set()
        for flag in SHF:
            if flag.value & sh_flags:
                f.add(flag)
        s["flags"] = f
        s["addr"] = endian_read(buf, endian, ADDR_SIZE)
        s["offset"] = endian_read(buf, endian, ADDR_SIZE)
        s["size"] = endian_read(buf, endian, ADDR_SIZE)
        s["link"] = endian_read(buf, endian, 4)
        s["info"] = endian_read(buf, endian, 4)
        s["addralign"] = endian_read(buf, endian, ADDR_SIZE)
        s["entsize"] = endian_read(buf, endian, ADDR_SIZE)
        sections.append(s)

    return sections
