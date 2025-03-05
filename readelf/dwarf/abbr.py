from .leb128 import leb128_parse
from .err import DWARFError
from ..const import *
from ..helpers import is_eof


class AbbreviationTableEntry:
    def __init__(
        self,
        parent,
        eldest_sibling,
        abbr_code=None,
        tag=None,
        has_children=None,
        attributes=None,
        is_root=False,
        offset=-1,
    ):
        self.is_root = is_root
        self.tag = tag
        self.abbr_code = abbr_code
        self.has_children = has_children
        self.attributes = attributes
        self.offset = offset

        self.first_child = None
        self.is_first_child = eldest_sibling is None
        self.eldest_sibling = eldest_sibling
        self._fc_siblings = [self]
        self.parent = parent
        self.code_cache = {}
        if self.parent is not None:
            self.parent.add_child(self)  # takes care of the siblings too

    def __repr__(self):
        if self.is_root:
            return f"ROOT(0x{self.offset:X})"
        a = "\n\t".join(map(repr, self.attributes))
        return f"AbbreviationTableEntry({self.abbr_code=}, {self.tag=}, {self.has_children=})\n\t{a}"

    def by_code(self, code):
        if code not in self.code_cache:
            raise DWARFError(f"abbreviation table entry with {code=} not found")
        return self.code_cache[code]

    def add_sibling(self, sibling):
        if self.is_first_child:
            self._fc_siblings.append(sibling)
        else:
            self.eldest_sibling.add_sibling(sibling)

    def update_code_cache(self, child):
        self.code_cache[child.abbr_code] = child
        if not self.is_root:
            self.parent.update_code_cache(child)

    def add_child(self, child):
        self.update_code_cache(child)
        if self.first_child is None:
            self.first_child = child
        else:
            self.first_child.add_sibling(child)

    @property
    def siblings(self):
        if self.eldest_sibling is None:
            return self._fc_siblings
        return self.eldest_sibling._fc_siblings

    @property
    def children(self):
        if self.first_child is None:
            return set()
        return self.first_child._fc_siblings

    @classmethod
    def parse(cls, stream, parent, eldest_sibling):
        abbr_code = leb128_parse(stream)
        if abbr_code == 0:
            return None
        tag_int = leb128_parse(stream)
        if tag_int not in DW_TAG:
            raise DWARFError(f"unknown DW_TAG in abbreviation table: 0x{tag_int:X}")
        tag = DW_TAG(tag_int)
        print("TAG:", tag)
        has_children_bytes = stream.read(1)
        if not has_children_bytes:
            raise EOFError("Section ends while reading has_children")
        has_children = has_children_bytes[0]
        attributes = []
        while True:
            attr_int, form_int = leb128_parse(stream), leb128_parse(stream)
            if attr_int == 0 and form_int == 0:
                break
            else:
                if attr_int not in DW_AT:
                    raise DWARFError(
                        f"unknown DW_AT in abbreviation table : 0x{attr_int:X}"
                    )
                if form_int not in DW_FORM:
                    raise DWARFError(
                        f"unknown DW_FORM in abbreviation table: 0x{form_int:X}"
                    )
                attr, form = DW_AT(attr_int), DW_FORM(form_int)
                if form == DW_FORM.DW_FORM_implicit_const:
                    attributes.append((attr, (form, leb128_parse(stream, signed=True))))
                attributes.append((attr, (form, None)))
                print("\t", attributes[-1])
        return cls(
            parent,
            eldest_sibling,
            abbr_code=abbr_code,
            tag=tag,
            has_children=has_children,
            attributes=attributes,
        )


class AbbreviationTables:
    def __init__(self, tables):
        self.tables = tables

    def table_by_offset(self, offset):
        for table in self.tables:
            if table.offset == offset:
                return table
        raise DWARFError(f"no abbr table at offset 0x{offset:X}")
    
    def entry_by_cu_and_code(self, cu, code):
        table = table_by_offset(cu.abbr_offset)
        return table.by_code(code)

def parse_abbr_section(stream):
    abbrev_tables = []
    start = stream.tell()
    root = AbbreviationTableEntry(None, None, is_root=True, offset=0)
    parents = [root]  # a stack of parents
    while parents and not is_eof(stream):
        eldest_sibling = getattr(parents[-1], "first_child", None)
        item = AbbreviationTableEntry.parse(stream, parents[-1], eldest_sibling)
        if item is None:  # new table
            abbrev_tables.append(root)
            root = AbbreviationTableEntry(
                None, None, is_root=True, offset=stream.tell() - start
            )  # new root
            parents = [root]
        elif item.has_children:
            parents.append(item)
    return AbbreviationTables(abbrev_tables)
