from io import BytesIO
from ..const import ARCH_32, ARCH_64
from ..helpers import endian_read


class Sym:
    def __init__(self, name, info, other, shndx, value, size, file):
        self.name = ""
        self._name = name
        self._info = info
        self._other = other
        self.shndx = shndx
        self.value = value
        self.size = size
        self.file = file
        self.bind = self._info >> 4  # enum
        self.type = self._info & 0xF  # enum
        self.visibility = self._other & 0x3  # enum

    def _load_name(self, dynstr):
        self.name = dynstr.get_name(self._name)


class SymTab:
    __sym_class = Sym
    def __init__(self, content, file):
        self.buf = BytesIO(content)
        self.file = file
        self.arch = file.arch
        self.endian = file.endian
        self._is_arch_64 = self.arch == ARCH_64
        self._name_size = 4
        self._size_size = self._value_size = 8 if self._is_arch_64 else 4
        self._shndx_size = 2
        self._uchar_size = 1
        self.symbols = []
        while True:
            name, value, size, info, other, shndx, offset = self._read_one_symbol()
            self.symbols.append(
                self.__class__.__sym_class(name, info, other, shndx, value, size, self.file)
            )
            if offset == len(content):
                break

    def get_strtab(self):
        return self.file.find_section(".strtab")

    def _after_init(self):
        self._strtab = self.get_strtab()
        for sym in self.symbols:
            sym._load_name(self._strtab)

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
