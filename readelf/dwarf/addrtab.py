import io
from readelf.helpers import endian_read
from .err import DWARFError


class AddrTab:
    def __init__(
        self, unit_length, address_size, segment_selector_size, entries, parent=None
    ):
        self.unit_length = unit_length
        self.address_size = address_size
        self.segment_selector_size = segment_selector_size
        self.entries = entries
        self.parent = parent

    @classmethod
    def from_stream(cls, stream, parent):
        endian = parent.parent.elf_file.endian
        unit_length = endian_read(stream, 4, endian)
        if unit_length == 0xFFFFFFFF:
            unit_length = endian_read(stream, 8, endian)
        version = endian_read(stream, 2, endian)
        if version != 5:
            raise DWARFError(
                f"can't read address table: only DWARF version 5 is currently supported ({version=})"
            )
        address_size = ord(stream.read(1))
        segment_selector_size = ord(stream.read(1))
        entries = [] # TODO
        return cls(unit_length, address_size, segment_selector_size, entries, parent)

class AddrTabs:
    def __init__(self, content, dwarf):
        self.content = content
        self.parent = dwarf
        self.stream = io.BytesIO(content)
        self.at_offset_cache = {}

    def __getitem__(self, offset):
        if offset in self.at_offset_cache:
            return self.at_offset_cache(offset)
        self.stream.seek(offset)
        tab = AddrTab.from_stream(self.stream, self)
        self.at_offset_cache[offset] = tab
        return tab
