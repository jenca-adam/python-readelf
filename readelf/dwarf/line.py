from .err import DWARFError
from .leb128 import leb128_parse
from readelf.helpers import endian_read, read_struct
from readelf.const import DW_FORM, DW_LNCT


class LineNumberProgram:
    def __init__(
        self,
    ):
        pass

    @classmethod
    def parse(cls, dwarf, stream):
        unit_length = endian_read(stream, dwarf.elf_file.endian, 4)
        unit_length_size = 4
        if unit_length == 0xFFFFFFFF:
            unit_length = endian_read(stream, dwarf.elf_file.endian, 8)
            unit_length_size = 8
        version = endian_read(stream, dwarf.elf_file.endian, 2)
        if version != 5:
            raise DWARFError(
                f"can't read line header: only version 5 is currently supported ({version=})"
            )
        addr_size, segment_sel_size = read_struct(stream, "BB")
        header_length = endian_read(stream, dwarf.elf_file.endian, unit_length_size)
        (
            min_instr_length,
            max_op_per_instr,
            default_is_stmt,
            line_base,
            line_range,
            opcode_base,
        ) = read_struct("BBBbBB", stream)
        std_opcode_lengths = read_struct(f"{opcode_base}B", stream)
        def_cnt = read_struct("b", stream)
        dir_entry_fmt = []
        for i in range(def_cnt):
            type_code_int = leb128_parse(stream)
            if type_code_int not in DW_LNCT:
                raise DWARFError(f"unknown DW_LNCT in line header: {type_code_int}")
            type_code = DW_LNCT(type_code_int)
            form_int = leb128_parse(stream)
            if form_int not in DW_FORM:
                raise DWARFError(f"unknown DW_FORM in line header: {form_int}")
            form = DW_FORM(form_int)
            dir_entry_fmt.append(type_code, form)
