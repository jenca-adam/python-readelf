from . import dynamic, dynsym, strtab, symtab, rel, rela
from ..const import SHT


class UnknownSection:
    def __init__(self, content, file, *_):
        self.content = content
        self.file = file


SECTION_TO_PARSER_MAPPING = {
    (SHT.SHT_DYNAMIC): dynamic.Dynamic,
    (SHT.SHT_DYNSYM): dynsym.DynSymTab,
    (SHT.SHT_STRTAB): strtab.StrTab,
    (SHT.SHT_SYMTAB): symtab.SymTab,
    (SHT.SHT_REL): rel.Rel,
    (SHT.SHT_RELA): rela.Rela,
}


def parse_content(sht, content, file, sd):
    return SECTION_TO_PARSER_MAPPING.get(sht, UnknownSection)(content, file, sd)
