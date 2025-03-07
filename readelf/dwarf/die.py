from .leb128 import leb128_parse
from .attribs import parse_attrib
import pprint


class DIE:
    def __init__(self, cu, abbr_entry, attrs, size, is_sentinel=False):
        self.cu = cu
        self.attrs = attrs
        self.abbr_entry = abbr_entry
        self.size = size
        self.is_sentinel = is_sentinel
        self.children = []
        self.has_children = self.abbr_entry and self.abbr_entry.has_children

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
            attrs[attr] = parse_attrib(attr, form, stream, cu)
            print(attr, attrs[attr])
        end = stream.tell()
        return cls(cu, abbr_entry, attrs, end - start)

    def __repr__(self):
        if self.is_sentinel:
            return "DIE(SENTINEL)"
        return f"DIE({self.abbr_entry.tag}, {pprint.pformat(self.attrs)})"


class DIEPtr:
    def __init__(self, cu, addr, absolute=False):
        if absolute:
            self.cu = cu.parent.cu_at_offset(addr)
            self.addr = addr - self.cu.section_offset
        else:
            self.addr = addr
            self.cu = cu
            self.absolute = absolute

    @property
    def content(self):
        return self.cu.die_at_offset(self.addr - self.cu.header_size)

    def __repr__(self):
        return f"DIEPtr({self.addr:#x})"
