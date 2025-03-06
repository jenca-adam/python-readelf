from .leb128 import leb128_parse
from .attribs import parse_attrib


class DIE:
    def __init__(self, cu, abbr_entry, attrs):
        self.cu = cu
        self.attrs = attrs
        self.abbr_entry = abbr_entry

    @classmethod
    def from_stream(cls, stream, cu):
        abbr_code = leb128_parse(stream)
        abbr_entry = cu.abbr_tab.by_code(abbr_code)
        attrs = {}
        for attrib in abbr_entry.attributes:
            attr, form = attrib
            attrs[attr] = parse_attrib(attr, form, stream, cu)
        return cls(cu, abbr_entry, attrs)
