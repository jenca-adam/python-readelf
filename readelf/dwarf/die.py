from .leb128 import leb128_parse
from .attribs import parse_attrib


class DIE:
    def __init__(self, cu, abbr_entry, attrs, size):
        self.cu = cu
        self.attrs = attrs
        self.abbr_entry = abbr_entry
        self.size=size

    @classmethod
    def from_stream(cls, stream, cu):
        start=stream.tell()
        abbr_code = leb128_parse(stream)
        abbr_entry = cu.abbr_tab.by_code(abbr_code)
        attrs = {}
        for attrib in abbr_entry.attributes:
            attr, form = attrib
            attrs[attr] = parse_attrib(attr, form, stream, cu)
            print(attr, attrs[attr])
        end=stream.tell()
        return cls(cu, abbr_entry, attrs, end-start)


class DIEPtr:
    def __init__(self, cu, addr, absolute=False):
        self.addr = addr
        self.cu = cu
        self.absolute = absolute
        self._content = None

    @property
    def content(self):
        if self._content is None:
            if self.absolute:
                debug_info = self.cu.parent.debug_info  # what about supp
                ref_stream = io.BytesIO(debug_info.content)
                ref_stream.seek(offset_int)
                self._content = DIE.from_stream(
                    ref_stream, cu.parent.cu_at_offset(offset_int)
                )  # ??
            else:
                try:
                    self._content = next(cu.get_dies(n=1, offset=off - cu.header_size))
                except StopIteration:
                    raise LookupError(f"no DIE at offset {off:#x} in CU")
        return self._content

    def __repr__(self):
        return f"DIEPtr({self.addr:#x})"
