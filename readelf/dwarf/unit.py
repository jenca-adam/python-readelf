import io
from readelf.helpers import endian_read, is_eof
from readelf.const import *
from .err import DWARFError
from .leb128 import leb128_parse
from .die import DIE, DIEPtr


class CompilationUnit:
    _dieptrclass = DIEPtr  # UGLY

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
        section_offset,
        header_size,
        content_size,
    ):
        self.unit_length = unit_length
        self.arch = arch
        self.version = version
        self.unit_type = unit_type
        self.abbr_offset = abbr_offset
        self.addr_size = addr_size
        self.dwo_id = dwo_id
        self.content = content
        self.stream = io.BytesIO(self.content)
        self.parent = parent
        self.type_signature = type_signature
        self.type_offset = type_offset
        self.section_offset = section_offset
        self.header_size = header_size
        self.content_size = content_size
        self.die_cache = {}

    @property
    def abbr_tab(self):
        return self.parent.abbrevs.table_by_offset(self.abbr_offset)

    def die_at_offset(self, offset):
        old_seek = self.stream.tell()
        self.stream.seek(offset)
        if offset not in self.die_cache:
            self.die_cache[offset] = DIE.from_stream(self.stream, self)
        self.stream.seek(old_seek)
        return self.die_cache[offset]

    def get_dies(self):
        parents = []  # stack
        offset = 0
        while offset < self.content_size:
            die = self.die_at_offset(offset)
            offset += die.size
            if die.is_sentinel:
                if not parents:
                    break  # ??
                else:
                    if (
                        len(parents) == 1
                    ):  # if sentinel closes a top level die, yield it
                        yield parents[-1]
                    parents.pop()  # pop stack
                    continue
            if parents:
                parents[-1].children.append(die)
                continue
            if die.has_children:
                parents.append(die)
                continue
            yield die

    @classmethod
    def parse(cls, dwarf, stream):
        offset = stream.tell()
        unit_length = endian_read(stream, dwarf.elf_file.endian, 4)
        if unit_length == 0xFFFFFFFF:
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
            offset,
            header_end,
            content_size,
        )
