from ..helpers import extract_sections, is_eof
from .abbr import parse_abbr_section
from .unit import CompilationUnit
from .line import LnoProgram
from .macro import MacroUnit
from .aranges import AddressRangesSet
from .die import DIEPtr
import io


class DWARF:
    def __init__(self, elf_file):
        self._dieptrclass = DIEPtr
        self.elf_file = elf_file
        (
            self.debug_info,
            self.debug_abbrev,
            self.debug_line,
            self.debug_loc,
            self.debug_str,
            self.debug_line_str,
            self.debug_macro,
            self.debug_aranges,
        ) = extract_sections(
            elf_file,
            ".debug_info",
            ".debug_abbrev",
            ".debug_line",
            ".debug_loc",
            ".debug_str",
            ".debug_line_str",
            ".debug_macro",
            ".debug_aranges",
            required=[0, 1],
            errmsg="file has missing debug information: missing section: {!r}",
        )
        self.units = []
        self._debug_info_stream = io.BytesIO(self.debug_info.content)
        while not is_eof(self._debug_info_stream):
            self.units.append(CompilationUnit.parse(self, self._debug_info_stream))
        self.lnos = []
        self._lnocache = {}
        if self.debug_line:
            self._debug_line_stream = io.BytesIO(self.debug_line.content)
            while not is_eof(self._debug_line_stream):
                offset = self._debug_line_stream.tell()
                lnop = LnoProgram.parse(self, self._debug_line_stream)
                self._lnocache[offset] = lnop

        self.macros = []
        if self.debug_macro:
            self._debug_macro_stream = io.BytesIO(self.debug_macro.content)
            while not is_eof(self._debug_macro_stream):
                self.macros.append(
                    MacroUnit.parse(
                        self,
                        self._debug_macro_stream,
                    )
                )
        self.address_ranges = []
        if self.debug_aranges:
            self._debug_aranges_stream = io.BytesIO(self.debug_aranges.content)
            while not is_eof(self._debug_aranges_stream):
                self.address_ranges.append(
                    AddressRangesSet.parse(self, self._debug_aranges_stream)
                )

        _debug_abbrev = io.BytesIO(self.debug_abbrev.content)
        self.abbrevs = parse_abbr_section(_debug_abbrev)

    def lnop_at_offset(self, offset):
        if offset in self._lnocache:
            return self._lnocache[offset]
        self._debug_line_stream.seek(offset)
        lnop = LnoProgram.parse(self, self._debug_line_stream)
        self._lnocache[offset] = lnop
        return lnop

    def cu_at_offset(self, offset):
        for unit in self.units:
            if unit.section_offset <= offset <= unit.section_offset + unit.unit_length:
                return unit
        raise LookupError(f"No compilation unit at offset {offset:#x}")
