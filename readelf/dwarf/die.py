from .leb128 import leb128_parse
from .attribs import parse_attrib
from .parsers import parse_die
from readelf.helpers import map_public_attributes
import pprint


class DIE:
    def __init__(self, cu, abbr_entry, attrs, size, is_sentinel=False):
        self.cu = cu
        self.attrs = attrs
        self.abbr_entry = abbr_entry
        self.tag = self.abbr_entry.tag if self.abbr_entry else None
        self.size = size
        self.is_sentinel = is_sentinel
        self.children = []
        self.has_children = self.abbr_entry and self.abbr_entry.has_children
        self.parsed = parse_die(self)
        map_public_attributes(self.parsed, self)

    @classmethod
    def from_stream(cls, stream, cu):
        start = stream.tell()
        abbr_code = leb128_parse(stream)
        if abbr_code == 0:
            return cls(cu, None, {}, 1, True)
        abbr_entry = cu.abbr_tab.by_code(abbr_code)
        attrs = {}
        for attrib in abbr_entry.attributes:

            attr, form = attrib

            attrs[attr] = parse_attrib(attr, form, stream, cu.meta)
            print(attr, form, attrs[attr])
        end = stream.tell()
        return cls(cu, abbr_entry, attrs, end - start)

    def __repr__(self):
        if self.is_sentinel:
            return "DIE(SENTINEL)"
        return f"DIE({self.tag}, {pprint.pformat(self.attrs)})"


class DIEPtr:
    def __init__(self, meta, addr, absolute=False):
        self.meta = meta
        self.cu = meta.dwarf.cu_at_offset(addr)
        if absolute:
            self.addr = addr - self.cu.section_offset
        else:
            self.addr = addr
        self.absolute = absolute

    @property
    def content(self):
        return self.cu.die_at_offset(self.addr - self.cu.header_size)

    def __repr__(self):
        return f"DIEPtr({self.addr:#x})"
