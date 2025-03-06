from ..helpers import extract_sections, is_eof
from .abbr import parse_abbr_section
from .unit import CompilationUnit
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
        ) = extract_sections(
            elf_file,
            ".debug_info",
            ".debug_abbrev",
            ".debug_line",
            ".debug_loc",
            ".debug_str",
            ".debug_line_str",
            required=[0, 1],  # should we also require .debug_abbrev?
            errmsg="file has missing debug information: missing section: {!r}",
        )
        self.units = []
        _debug_info_stream = io.BytesIO(self.debug_info.content)
        while not is_eof(_debug_info_stream):
            self.units.append(CompilationUnit.parse(self, _debug_info_stream))
        _debug_abbrev = io.BytesIO(self.debug_abbrev.content)
        self.abbrevs = parse_abbr_section(_debug_abbrev)
        print(self.abbrevs.tables)
