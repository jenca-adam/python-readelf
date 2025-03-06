from readelf.const import ARCH
from readelf.helpers import endian_read
import warnings


def parse_strp_with_table(stream, cu, table):
    size = 4 if cu.arch == ARCH.ARCH_32 else 8
    offset = endian_read(stream, cu.parent.elf_file.endian, size)
    return table.get_name(offset)


def parse_strp(stream, cu, supp):
    return parse_strp_with_table(stream, cu, cu.parent.debug_str)


def parse_line_strp(stream, cu, supp):
    return parse_strp_with_table(stream, cu, cu.parent.debug_line_str)


def parse_strp_sup(stream, cu, supp):
    warnings.warn(UserWarning("strp_sup parsing not supported yet. Parsing as strp"))
    return parse_strp(stream, cu)
