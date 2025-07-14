from readelf.const import ARCH
from readelf.helpers import endian_read
import warnings


def parse_strp_with_table(stream, meta, table):
    size = 4 if meta.arch == ARCH.ARCH_32 else 8
    offset = endian_read(stream, meta.endian, size)
    return table.get_name(offset)


def parse_strp(stream, meta, supp, cu):
    return parse_strp_with_table(stream, meta, meta.dwarf.debug_str)


def parse_line_strp(stream, meta, supp, cu):
    return parse_strp_with_table(stream, meta, meta.dwarf.debug_line_str)


def parse_strp_sup(stream, meta, supp, cu):
    warnings.warn(UserWarning("strp_sup parsing not supported yet. Parsing as strp"))
    return parse_strp(stream, meta)
