from ..helpers import extract_sections, is_eof
from .abbr import parse_abbr_section
from .unit import CompilationUnit
from .line import LnoProgram
from .macro import MacroUnit
import io


class DWARF:
    def __init__(self, elf_file):
        self.elf_file = elf_file
        (
            self.debug_info,
            self.debug_abbrev,
            self.debug_line,
            self.debug_loc,
            self.debug_str,
            self.debug_line_str,
            self.debug_macro,
        ) = extract_sections(
            elf_file,
            ".debug_info",
            ".debug_abbrev",
            ".debug_line",
            ".debug_loc",
            ".debug_str",
            ".debug_line_str",
            ".debug_macro",
            required=[0, 1],
            errmsg="file has missing debug information: missing section: {!r}",
        )
        self.units = []
        _debug_info_stream = io.BytesIO(self.debug_info.content)
        while not is_eof(_debug_info_stream):
            self.units.append(CompilationUnit.parse(self, _debug_info_stream))
        self.lnos = []
        if self.debug_line:
            _debug_line_stream = io.BytesIO(self.debug_line.content)
            while not is_eof(_debug_line_stream):
                self.lnos.append(LnoProgram.parse(self, _debug_line_stream))
        self.macros = []
        if self.debug_macro:
            _debug_macro_stream = io.BytesIO(self.debug_macro.content)
            self.macros.append(MacroUnit.parse(self, _debug_macro_stream, self.units[0]))
        _debug_abbrev = io.BytesIO(self.debug_abbrev.content)
        self.abbrevs = parse_abbr_section(_debug_abbrev)
        print(self.abbrevs.tables)

    def cu_at_offset(self, offset):
        for unit in self.units:
            if unit.section_offset <= offset <= unit.section_offset + unit.unit_length:
                return unit
        raise LookupError(f"No compilation unit at offset {offset:#x}")
