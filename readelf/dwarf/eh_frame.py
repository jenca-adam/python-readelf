from io import BytesIO
from readelf.const import ARCH, DW_EH_PE
from readelf.helpers import endian_read, read_string, is_eof
from readelf.dwarf.leb128 import leb128_parse


class CIE:
    def __init__(self, stream, length, cie_ptr, offset, start, arch, endian, parent):
        self.arch = arch
        self.endian = endian
        self.length = length
        self.cie_ptr = cie_ptr
        self.offset = offset
        self.version = endian_read(stream, self.endian, 1)
        self.aug_string = read_string(stream)
        self.parent = parent
        if b"eh" in self.aug_string:
            if arch == ARCH.ARCH_32:
                self.eh_data = endian_read(stream, self.endian, 4)

            elif arch == ARCH.ARCH_64:
                self.eh_data = endian_read(stream, self.endian, 8)
        else:
            self.eh_data = None

        self.code_alignment_factor = leb128_parse(stream)
        self.data_alignment_factor = leb128_parse(stream)
        if b"z" in self.aug_string:
            self.augmentation_length = leb128_parse(stream)
            self.augmentation_data = stream.read(self.augmentation_length)
        else:
            self.augmentation_length = 0
            self.augmentation_data = b""
        end = stream.tell()
        self.content = stream.read(self.length - (end - start))


class FDE:
    def __init__(self, stream, length, cie_ptr, offset, start, arch, endian, parent):
        self.arch = arch
        self.endian = endian
        self.length = length
        self.parent = parent
        self.cie_ptr = cie_ptr
        self.offset = offset
        self.cie = parent.get_cie(self.offset - cie_ptr)
        if self.arch == ARCH.ARCH_32:
            addr_size = 4
        elif self.arch == ARCH.ARCH_64:
            addr_size = 8
        self.pc_begin = endian_read(stream, self.endian, addr_size)
        if b"z" in self.cie.aug_string:
            self.augmentation_length = leb128_parse(stream)
            self.augmentation_data = stream.read(self.augmentation_length)
        else:
            self.augmentation_length = 0
            self.augmentation_data = b""
        end = stream.tell()
        self.content = stream.read(self.length - (end - start))


class EhFrame:
    def __init__(self, dwarf, stream):
        # can't make this a class method because of the CIE cache
        # for now

        self.stream = stream
        self.arch = dwarf.elf_file.arch
        self.endian = dwarf.elf_file.endian
        self.cies = {}
        self.fdes = []
        while not is_eof(stream):
            entry = self.parse_entry()
            if entry.cie_ptr == 0:
                self.cies[entry.offset] = entry

    def get_cie(self, offset):
        if offset not in self.cies:
            raise LookupError(f"No CIE at offset {offset:#x}")
        return self.cies[offset]

    def parse_entry(self):
        offset = stream.tell()
        length = endian_read(self.stream, self.endian, 4)
        if length == 0xFFFFFFFF:
            length = endian_read(self.stream, self.endian, 8)
        start = stream.tell()
        cie_ptr = endian_read(self.stream, self.endian, 4)
        if cie_ptr == 0:
            return CIE(
                self.stream, length, 0, start, offset, self.arch, self.endian, self
            )
        return FDE(
            self.stream, length, cie_ptr, start, offset, self.arch, self.endian, self
        )

class EhFrameHdr:
    @classmethod 
    def parse(self, dwarf, stream):
        pass
