import io
from ..helpers import endian_read
from ..const import ARCH


class RelEntry:
    def __init__(self, offset, info, arch):
        self.offset = offset
        self.info = info
        if arch == ARCH.ARCH_32:
            self.sym = self.info >> 8
            self.type = self.info & 0xFF
        else:
            self.sym = self.info >> 32
            self.type = self.info & 0xFFFFFFFF

    def _update_sym(self, symtab):
        self.sym = symtab.symbols[self.sym]


class Rel:
    def __init__(self, content, file, sec_dict):
        self.content = content
        self.file = file
        self.arch = self.file.arch
        self.stream = io.BytesIO(content)
        self.entries = []
        self.modify = sec_dict["info"]
        self.symtab = sec_dict["link"]
        while self.stream.tell() < len(self.content) - 1:
            if self.arch == ARCH.ARCH_32:
                offset = endian_read(self.stream, file.endian, 4)
                info = endian_read(self.stream, file.endian, 4)
            else:
                offset = endian_read(self.stream, file.endian, 8)
                info = endian_read(self.stream, file.endian, 8)
            self.entries.append(RelEntry(offset, info, self.arch))

    def _after_init(self):
        self.symtab = self.file.sections[self.symtab]
        for en in self.entries:
            en._update_sym(self.symtab)
