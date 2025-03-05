from readelf.const import ARCH
from readelf.helpers import endian_read


def parse_strp_with_table(stream, cu, table):
    size = 4 if cu.arch == ARCH.ARCH_32 else 8
    offset = endian_read(stream, cu.parent.elf_file.endian, size)
    return table.get_name(offset)


def make_strp_parser(table):
    def strp_parser(stream, cu):
        tabsec = cu.parent.elf_file.find_section(table)
        return parse_strp_with_table(stream, cu, tabsec)

    return strp_parser
