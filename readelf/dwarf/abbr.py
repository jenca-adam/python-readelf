from .leb128 import leb128_parse
from .err import DWARFError
from ..const import *
from ..helpers import is_eof


class AbbreviationTableEntry:
    def __init__(
        self,
        table,
        abbr_code=None,
        tag=None,
        has_children=None,
        attributes=None,
        offset=-1,
    ):
        self.tag = tag
        self.abbr_code = abbr_code
        self.has_children = has_children
        self.attributes = attributes
        self.table = table
        if self.table is not None:
            self.table.add_entry(self)  # takes care of the siblings too

    def __repr__(self):
        a = "\n\t".join(map(repr, self.attributes))
        return f"AbbreviationTableEntry({self.abbr_code=}, {self.tag=}, {self.has_children=})\n\t{a}"

    @classmethod
    def parse(cls, stream, table):
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
            table,
            abbr_code=abbr_code,
            tag=tag,
            has_children=has_children,
            attributes=attributes,
        )


class AbbreviationTable:
    def __init__(self, offset):
        self.code_cache = {}
        self.entries = []
        self.offset = offset

    def add_entry(self, entry):
        self.entries.append(entry)
        self.code_cache[entry.abbr_code] = entry

    def by_code(self, code):
        if code not in self.code_cache:
            raise DWARFError(f"abbreviation table entry with {code=} not found")
        return self.code_cache[code]


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
    table = AbbreviationTable(0)
    start = stream.tell()
    while not is_eof(stream):
        item = AbbreviationTableEntry.parse(stream, table)
        if item is None:  # new table
            abbrev_tables.append(table)
            table = AbbreviationTable(stream.tell() - start)

    return AbbreviationTables(abbrev_tables)
