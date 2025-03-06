import io
from ..helpers import endian_read
from ..const import *
from .err import DWARFError
from .leb128 import leb128_parse
from .die import DIE


class CompilationUnit:
    def __init__(
        self,
        unit_length,
        arch,
        version,
        unit_type,
        abbr_offset,
        addr_size,
        dwo_id,
        content,
        parent,
        type_signature,
        type_offset,
    ):
        self.unit_length = unit_length
        self.arch = arch
        self.version = version
        self.unit_type = unit_type
        self.abbr_offset = abbr_offset
        self.addr_size = addr_size
        self.dwo_id = dwo_id
        self.content = content
        self.parent = parent
        self.type_signature = type_signature
        self.type_offset = type_offset

    @property
    def abbr_tab(self):
        return self.parent.abbrevs.table_by_offset(self.abbr_offset)

    def get_dies(self):
        stream = io.BytesIO(self.content)
        return DIE.from_stream(stream, self)

    @classmethod
    def parse(cls, dwarf, stream):
        offset = stream.tell()
        unit_length = endian_read(stream, dwarf.elf_file.endian, 4)
        if unit_length == 0xFFFF:
            unit_length_size = section_offset_length = 8
            unit_length = endian_read(stream, dwarf.elf_file.endian, 8)
            arch = ARCH.ARCH_64

        else:
            unit_length_size = section_offset_length = 4
            arch = ARCH.ARCH_32
        version = endian_read(stream, dwarf.elf_file.endian, 2)
        if version != 5:
            raise DWARFError(
                f"can't read dwarf header: only version 5 is currently supported ({version=})"
            )
        unit_type_int = endian_read(stream, dwarf.elf_file.endian, 1)
        if unit_type_int not in DW_UT:
            raise DWARFError(
                f"dwarf header format error: unknown DW_UT: {unit_type_int}"
            )
        unit_type = DW_UT(unit_type_int)
        addr_size = endian_read(stream, dwarf.elf_file.endian, 1)
        abbr_offset = endian_read(stream, dwarf.elf_file.endian, section_offset_length)
        if unit_type in (
            DW_UT.DW_UT_skeleton,
            DW_UT.DW_UT_split_compile,
            DW_UT.DW_UT_split_type,
        ):
            dwo_id = endian_read(stream, dwarf.elf_file.endian, 8)
        else:
            dwo_id = None
        if unit_type == DW_UT.DW_UT_type:
            type_signature = endian_read(stream, dwarf.elf_file.endian, 8)
            type_offset = endian_read(
                stream, dwarf.elf_file.endian, section_offset_length
            )
        else:
            type_signature = type_offset = None

        header_end = stream.tell() - offset
        content_size = unit_length - (header_end - unit_length_size)
        content = stream.read(content_size)
        if len(content) < content_size:
            raise DWARFError(
                f"unit content too short: expected {content_size} bytes, section cuts off at {len(content)}"
            )
        return cls(
            unit_length,
            arch,
            version,
            unit_type,
            abbr_offset,
            addr_size,
            dwo_id,
            content,
            dwarf,
            type_signature,
            type_offset,
        )
