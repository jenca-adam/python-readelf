from io import BytesIO
from ..const import *
from ..helpers import endian_read

SHN_LORESERVE = 0xFF00
SHN_HIRESERVE = 0xFFFF
SHN_LOPROC = 0xFF00
SHN_HIPROC = 0xFF1F
SHN_LOOS = 0xFF20
SHN_HIOS = 0xFF3F
STB_LOPROC = 13
STB_HIPROC = 15
STB_LOOS = 10
STB_HIOS = 12
STT_LOOS = 10
STT_HIOS = 12
STT_LOPROC = 13
STT_HIPROC = 15


def _get_shndx_const(shndx):
    if shndx in SHN:
        return SHN(shndx)
    else:
        return shndx


class Sym:
    def __init__(self, name, info, other, shndx, value, size, file):
        self.name = ""
        self._name = name
        self._info = info
        self._other = other
        self.shndx = _get_shndx_const(shndx)
        self._value = value
        self.size = size
        self.file = file
        self.bind = self._info >> 4  # enum
        self.type = self._info & 0xF  # enum
        self.visibility = STV(self._other & 0x3)  # enum
        if STB_LOOS <= self.bind <= STB_HIOS:
            self.bind = STB.STB_OS
        elif STB_LOPROC <= self.bind <= STB_HIPROC:
            self.bind = STB.STB_PROC
        else:
            self.bind = STB(self.bind)

        if STT_LOOS <= self.type <= STT_HIOS:
            self.type = STT.STT_OS
        elif STT_LOPROC <= self.type <= STT_HIPROC:
            self.type = STT.STT_PROC
        else:
            self.type = STT(self.type)

    def _load_name(self, dynstr):
        self.name = dynstr.get_name(self._name)

    def _load_value(self):
        if isinstance(self.shndx, int):
            self.section = self.file.sections[self.shndx]
            start_index = self._value - self.section.addr
            self.value = self.section.content[start_index : start_index + self.size]
        else:
            self.section = None
            self.value = b""

    def __repr__(self):
        return f"<{self.__class__.__name__} [{self.type.name}] {self.name} ({self.shndx}@{self._value:x}+{self.size})>"


class SymTab:
    __sym_class = Sym

    def __init__(self, content, file, *_):
        self.buf = BytesIO(content)
        self.file = file
        self.arch = file.arch
        self.endian = file.endian
        self._is_arch_64 = self.arch == ARCH.ARCH_64
        self._name_size = 4
        self._size_size = self._value_size = 8 if self._is_arch_64 else 4
        self._shndx_size = 2
        self._uchar_size = 1
        self.symbols = []
        while True:
            name, value, size, info, other, shndx, offset = self._read_one_symbol()
            self.symbols.append(
                self.__class__.__sym_class(
                    name, info, other, shndx, value, size, self.file
                )
            )
            if offset >= len(content):
                break

    def get_strtab(self):
        return self.file.find_section(".strtab")

    def _after_init(self):
        self._strtab = self.get_strtab()

        for sym in self.symbols:
            sym._load_name(self._strtab)
            sym._load_value()

    def _read_one_symbol(self):
        if self._is_arch_64:
            name = endian_read(self.buf, self.endian, self._name_size)
            info = endian_read(self.buf, self.endian, self._uchar_size)
            other = endian_read(self.buf, self.endian, self._uchar_size)
            shndx = endian_read(self.buf, self.endian, self._shndx_size)
            value = endian_read(self.buf, self.endian, self._value_size)
            size = endian_read(self.buf, self.endian, self._size_size)
        else:
            name = endian_read(self.buf, self.endian, self._name_size)
            value = endian_read(self.buf, self.endian, self._value_size)
            size = endian_read(self.buf, self.endian, self._size_size)
            info = endian_read(self.buf, self.endian, self._uchar_size)
            other = endian_read(self.buf, self.endian, self._uchar_size)
            shndx = endian_read(self.buf, self.endian, self._shndx_size)
        offset = self.buf.tell()

        return name, value, size, info, other, shndx, offset

    def get_symbol(self, symname):
        for symbol in self.symbols:
            if symbol.name == symname:
                return symbol
