from . import dynstr, dynsym, strtab, symtab


class UnknownSection:
    def __init__(self, content, file):
        self.content = content
        self.file = file


NAME_TO_PARSER_MAPPING = {
    ".dynstr": dynstr.DynStrTab,
    ".dynsym": dynsym.DynSymTab,
    ".strtab": strtab.StrTab,
    ".shstrtab": strtab.StrTab,
    ".symtab": symtab.SymTab
}


def parse_content(name, content, file):
    print(name)
    return NAME_TO_PARSER_MAPPING.get(name, UnknownSection)(content, file)
