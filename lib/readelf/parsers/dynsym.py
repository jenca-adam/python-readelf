from .symtab import SymTab, Sym


class DynSym(Sym):
    pass


class DynSymTab(SymTab):
    __sym_class = DynSym

    def get_strtab(self):
        return self.file.find_section(".dynstr")
