from readelf.helpers import read_struct, endian_read
from .err import DWARFError
from dataclasses import dataclass


@dataclass
class AddressRange:
    segment_selector: int | None
    start: int
    size: int


class AddressRangesSet:
    def __init__(self, ranges, unit):
        self.ranges = ranges
        self.unit = unit

    @classmethod
    def parse(cls, dwarf, stream):
        offset_size = 4
        head_start = stream.tell()
        (unit_length,) = read_struct(stream, "I", dwarf.elf_file.endian)
        if unit_length == 0xFFFFFFFF:
            (unit_length,) = read_struct(stream, "L", dwarf.elf_file.endian)
            offset_size = 8
        (version,) = read_struct(stream, "H", dwarf.elf_file.endian)
        if version != 2:
            raise DWARFError(
                f"can't read address ranges set table header: only version 2 is currently supported ({version=})"
            )
        cu_offset = endian_read(stream, dwarf.elf_file.endian, offset_size)
        cu = dwarf.cu_at_offset(cu_offset)
        (addr_size,) = read_struct(stream, "B")
        (ss_size,) = read_struct(stream, "B")
        tup_size = ss_size + 2 * addr_size
        padding = tup_size - (stream.tell() - head_start) % tup_size
        stream.read(padding)
        ranges = []
        while True:
            ss = None
            if ss_size > 0:
                ss = endian_read(stream, dwarf.elf_file.endian, ss_size)
            start, size = (
                endian_read(stream, dwarf.elf_file.endian, addr_size) for _ in range(2)
            )
            if not any((ss, start, size)):
                break
            ranges.append(AddressRange(ss, start, size))
        return cls(ranges, cu)
