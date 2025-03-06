from .leb128 import leb128_parse
from .attribs import parse_attrib


class DIE:
    def __init__(self, cu, abbr_entry, attrs, size, is_sentinel=False):
        self.cu = cu
        self.attrs = attrs
        self.abbr_entry = abbr_entry
        self.size=size
        self.is_sentinel=is_sentinel

    @classmethod
    def from_stream(cls, stream, cu):
        start=stream.tell()
        abbr_code = leb128_parse(stream)
        if abbr_code==0:
            return cls(cu, None, {}, 0, True)
        abbr_entry = cu.abbr_tab.by_code(abbr_code)
        attrs = {}
        for attrib in abbr_entry.attributes:
            attr, form = attrib
            attrs[attr] = parse_attrib(attr, form, stream, cu)
            print(attr, attrs[attr])
        end=stream.tell()
        return cls(cu, abbr_entry, attrs, end-start)

    def __repr__(self):
        if self.is_sentinel:
            return "DIE(SENTINEL)"
        return f"DIE({self.abbr_entry.tag}, {self.attrs})"
class DIEPtr:
    def __init__(self, cu, addr, absolute=False):
        if absolute:
            self.cu = cu.parent.cu_at_offset(addr)
            self.addr = addr-self.cu.section_offset
        else:
            self.addr = addr
            self.cu = cu
            self.absolute = absolute
        self._content = None

    @property
    def content(self):
        if self._content is None:
            try:
                self._content = next(self.cu.get_dies(n=1, offset=self.addr - self.cu.header_size))
            except StopIteration:
                raise LookupError(f"no DIE at offset {self.addr:#x} in CU")
        return self._content

    def __repr__(self):
        return f"DIEPtr({self.addr:#x})"
