from readelf.helpers import read_struct, endian_read
from readelf.const import DW_FORM
from .leb128 import leb128_parse


class MacroUnitFlags:
    def __init__(self, flags):
        self.offset_size_flag = flags & 0x1
        self.debug_line_offset_flag = flags & 0x2
        self.opcode_operands_table_flag = flags & 0x4
        self.offset_size = self.offset_size_flag * 4 + 4


class MacroUnit:
    def __init__(self, debug_line_offset, opcode_operands_table):
        self.debug_line_offset = debug_line_offset
        self.opcode_operands_table = opcode_operands_table

    @classmethod
    def parse(cls, dwarf, stream):
        (version,) = read_struct(stream, "H", dwarf.elf_file.endian)
        flags = MacroUnitFlags(read_struct(stream, "B")[0])
        if flags.debug_line_offset_flag:
            debug_line_offset = endian_read(
                stream, dwarf.elf_file.endian, flags.offset_size
            )
        else:
            debug_line_offset = None

        opcode_operands_table = {}
        if flags.opcode_operands_table_flag:
            (count,) = read_struct(stream, "B")
            for i in range(count):
                (opcode,) = read_struct(stream, "B")
                num_operands = leb128_parse(stream)
                operand_forms = [
                    DW_FORM(i) for i in read_struct(stream, f"{num_operands}B")
                ]
                opcode_operands_table[opcode] = operand_forms
        return cls(debug_line_offset, opcode_operands_table)
