from . import dynamic, dynsym, strtab, symtab
from ..const import SHT


class UnknownSection:
    def __init__(self, content, file):
        self.content = content
        self.file = file


SECTION_TO_PARSER_MAPPING = {
    (SHT.SHT_DYNAMIC): dynamic.Dynamic,
    (SHT.SHT_DYNSYM): dynsym.DynSymTab,
    (SHT.SHT_STRTAB): strtab.StrTab,
    (SHT.SHT_SYMTAB): symtab.SymTab,
}


def parse_content(sht, content, file):
    return SECTION_TO_PARSER_MAPPING.get(sht, UnknownSection)(content, file)
