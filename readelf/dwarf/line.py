from .err import DWARFError
from .leb128 import leb128_parse
from .attribs.form import parse_form
from .unit import CompilationUnit
from readelf.helpers import endian_read, endian_parse, read_struct
from readelf.const import DW_FORM, DW_LNCT, ARCH, DW_LNS, DW_LNE
import enum
import io
from dataclasses import dataclass


def _read_formatted(stream, dummycu):
    # used for the file_names and directories fields
    (fmt_cnt,) = read_struct(stream, "B")
    entry_fmt = []
    for i in range(fmt_cnt):
        type_code_int = leb128_parse(stream)
        if type_code_int not in DW_LNCT:
            raise DWARFError(f"unknown DW_LNCT in line header: {type_code_int}")
        type_code = DW_LNCT(type_code_int)

        form_int = leb128_parse(stream)
        if form_int not in DW_FORM:
            raise DWARFError(f"unknown DW_FORM in line header: {form_int}")
        form = DW_FORM(form_int)

        entry_fmt.append((type_code, form))
    entry_cnt = leb128_parse(stream)
    entries = []
    for i in range(entry_cnt):
        entry = []
        for field in entry_fmt:
            type_code, form = field
            entry.append(
                (type_code, parse_form(form, stream, dummycu, None))
            )  # no supp
        entries.append(entry)
    return entries


class BaseOps(enum.Enum):
    ADDR_ADD = 0
    ADDR_SET = 1
    OP_INDEX_ADD = 2
    OP_INDEX_SET = 3
    FILE_SET = 4
    LINE_ADD = 5
    LINE_SET = 6
    COLUMN_ADD = 7
    COLUMN_SET = 8
    IS_STMT_TOGGLE = 9
    IS_STMT_SET = 10
    BASIC_BLOCK_SET = 11
    END_SEQUENCE_SET = 12
    PROLOGUE_END_SET = 13
    EPILOGUE_BEGIN_SET = 14
    ISA_SET = 15
    DISCRIMINATOR_SET = 16
    ADVANCE_PC = 17
    APPEND_MATRIX = 18
    RESET_STMT = 19


class State:
    def __init__(self, default_is_stmt, files):
        self._files = files
        self.address = 0
        self.op_index = 0
        self.file = 1
        self.line = 1
        self.column = 0
        self.is_stmt = default_is_stmt
        self._default_is_stmt = default_is_stmt
        self.basic_block = False
        self.end_sequence = False
        self.prologue_end = False
        self.epilogue_begin = False
        self.isa = 0
        self.discriminator = 0
        self.matrix = []

    def reset_stmt(self):
        self.is_stmt = self._default_is_stmt

    def append_matrix(self):
        self.matrix.append(
            (
                self.address,
                self.op_index,
                self._files[self.file],
                self.line,
                self.column,
                self.is_stmt,
                self.basic_block,
                self.end_sequence,
                self.prologue_end,
                self.epilogue_begin,
                self.isa,
                self.discriminator,
            )
        )


class ProgramInstr:
    def __init__(self, *base_ops):
        self.base_ops = base_ops

    def execute(
        self, state, minimum_instruction_length, maximum_operations_per_instruction
    ):
        for op, *opargs in self.base_ops:
            if op == BaseOps.ADDR_ADD:
                state.addr += opargs[0]
            if op == BaseOps.ADDR_SET:
                state.addr = opargs[0]
            if op == BaseOps.OP_INDEX_ADD:
                state.op_index += opargs[0]
            if op == BaseOps.OP_INDEX_SET:
                state.op_index = opargs[0]
            if op == BaseOps.FILE_SET:
                state.file = opargs[0]
            if op == BaseOps.LINE_ADD:
                state.line += opargs[0]
            if op == BaseOps.LINE_SET:
                state.line = opargs[0]
            if op == BaseOps.COLUMN_ADD:
                state.column += opargs[0]
            if op == BaseOps.COLUMN_SET:
                state.column = opargs[0]
            if op == BaseOps.IS_STMT_TOGGLE:
                state.is_stmt = not state.is_stmt
            if op == BaseOps.IS_STMT_SET:
                state.is_stmt = bool(opargs[0])
            if op == BaseOps.BASIC_BLOCK_SET:
                state.basic_block = bool(opargs[0])
            if op == BaseOps.END_SEQUENCE_SET:
                state.end_sequence = bool(opargs[0])
            if op == BaseOps.PROLOGUE_END_SET:
                state.prologue_end = bool(opargs[0])
            if op == BaseOps.EPILOGUE_BEGIN_SET:
                state.epilogue_begin = bool(opargs[0])
            if op == BaseOps.ISA_SET:
                state.isa = opargs[0]
            if op == BaseOps.DISCRIMINATOR_SET:
                state.discriminator = opargs[0]
            if op == BaseOps.ADVANCE_PC:
                state.op_index = (
                    state.op_index + opargs[0]
                ) % maximum_operations_per_instruction
                state.address = state.address + minimum_instruction_length * (
                    (state.op_index + opargs[0]) // maximum_operations_per_instruction
                )
            if op == BaseOps.APPEND_MATRIX:
                state.append_matrix()
            if op == BaseOps.RESET_STMT:
                state.reset_stmt()

    @classmethod
    def from_special_opcode(
        cls,
        opcode,
        opcode_base,
        line_base,
        line_range,
    ):
        adjusted = opcode - opcode_base
        op_advance = adjusted // line_range
        line_increment = line_base + (adjusted % line_range)
        return cls(
            (BaseOps.LINE_ADD, line_increment),
            (BaseOps.ADVANCE_PC, op_advance),
            (BaseOps.APPEND_MATRIX,),
            (BaseOps.BASIC_BLOCK_SET, False),
            (BaseOps.PROLOGUE_END_SET, False),
            (BaseOps.EPILOGUE_BEGIN_SET, False),
            (BaseOps.DISCRIMINATOR_SET, 0),
        )

    @classmethod
    def from_standard_opcode(cls, opcode, operands, opcode_base, line_base, line_range):
        if opcode == DW_LNS.DW_LNS_copy:
            return cls(
                (BaseOps.APPEND_MATRIX,),
                (BaseOps.BASIC_BLOCK_SET, False),
                (BaseOps.PROLOGUE_END_SET, False),
                (BaseOps.EPILOGUE_BEGIN_SET, False),
                (BaseOps.DISCRIMINATOR_SET, 0),
            )
        elif opcode == DW_LNS.DW_LNS_advance_pc:
            return cls((BaseOps.ADVANCE_PC, *operands))
        elif opcode == DW_LNS.DW_LNS_advance_line:
            return cls((BaseOps.LINE_ADD, *operands))
        elif opcode == DW_LNS.DW_LNS_set_file:
            return cls((BaseOps.FILE_SET, *operands))
        elif opcode == DW_LNS.DW_LNS_set_column:
            return cls((BaseOps.COLUMN_SET, *operands))
        elif opcode == DW_LNS.DW_LNS_negate_stmt:
            return cls((BaseOps.IS_STMT_TOGGLE,))
        elif opcode == DW_LNS.DW_LNS_set_basic_block:
            return cls((BaseOps.BASIC_BLOCK_SET, *operands))
        elif opcode == DW_LNS.DW_LNS_const_add_pc:
            return cls.from_special_opcode(255, opcode_base, line_base, line_range)
        elif opcode == DW_LNS.DW_LNS_fixed_advance_pc:
            return cls((BaseOps.LINE_ADD, *operands), (BaseOps.OP_INDEX_SET, 0))
        elif opcode == DW_LNS.DW_LNS_set_prologue_end:
            return cls((BaseOps.PROLOGUE_END_SET, True))
        elif opcode == DW_LNS.DW_LNS_set_epilogue_begin:
            return cls((BaseOps.EPILOGUE_BEGIN_SET, True))
        elif opcode == DW_LNS.DW_LNS_set_isa:
            return cls((BaseOps.ISA_SET, *operands))

    @classmethod
    def from_extended_opcode(cls, opcode, operands, dwarf):
        if opcode == DW_LNE.DW_LNE_end_sequence:
            return cls(
                (BaseOps.END_SEQUENCE_SET, True),
                (BaseOps.APPEND_MATRIX,),
                (BaseOps.ADDR_SET, 0),
                (BaseOps.OP_INDEX_SET, 0),
                (BaseOps.FILE_SET, 1),
                (BaseOps.LINE_SET, 1),
                (BaseOps.COLUMN_SET, 0),
                (BaseOps.RESET_STMT,),
                (BaseOps.BASIC_BLOCK_SET, False),
                (BaseOps.END_SEQUENCE_SET, False),
                (BaseOps.PROLOGUE_END_SET, False),
                (BaseOps.EPILOGUE_BEGIN_SET, False),
                (BaseOps.ISA_SET, 0),
                (BaseOps.DISCRIMINATOR_SET, 0),
            )
        elif opcode == DW_LNE.DW_LNE_set_address:
            addr = endian_parse(operands, dwarf.elf_file.endian)
            return cls(
                (BaseOps.ADDR_SET, addr),
                (BaseOps.OP_INDEX_SET, 0),
            )
        elif opcode == DW_LNE.DW_LNE_set_discriminator:
            discriminator = leb128_parse(io.BytesIO(operands))
            return cls((BaseOps.DISCRIMINATOR_SET, discriminator))

    @classmethod
    def parse(
        cls,
        stream,
        std_opcode_lengths,
        opcode_base,
        line_base,
        line_range,
        state,
        minimum_instruction_length,
        maximum_operations_per_instruction,
        dwarf,
    ):
        (opcode,) = read_struct(stream, "B")
        if opcode == 0:  # extended
            length = leb128_parse(stream)
            (ext_opcode,) = read_struct(stream, "B")
            typ = DW_LNE(ext_opcode)
            operands = stream.read(length - 1)
            return cls.from_extended_opcode(typ, operands, dwarf)
        elif opcode < opcode_base:
            typ = DW_LNS(opcode)
            n_ops = std_opcode_lengths[opcode - 1]
            if typ == DW_LNS.DW_LNS_fixed_advance_pc:  # quirky *
                operands = [
                    endian_read(stream, dwarf.elf_file.endian, 2) for _ in range(n_ops)
                ]
            else:
                operands = [leb128_parse(stream) for _ in range(n_ops)]
            return cls.from_standard_opcode(
                typ, operands, opcode_base, line_base, line_range
            )
        else:
            return cls.from_special_opcode(
                opcode,
                opcode_base,
                line_base,
                line_range,
            )


class LnoProgram:
    def __init__(
        self,
        unit_length,
        arch,
        version,
        addr_size,
        segment_sel_size,
        dummycu,
        min_instr_length,
        max_op_per_instr,
        default_is_stmt,
        line_base,
        line_range,
        opcode_base,
        std_opcode_lengths,
        directories,
        file_names,
        prog,
    ):
        self.unit_length = unit_length
        self.arch = arch
        self.version = version
        self.addr_size = addr_size
        self.segment_sel_size = segment_sel_size
        self._dummycu = dummycu
        self.min_instr_length = min_instr_length
        self.max_op_per_instr = max_op_per_instr
        self.default_is_stmt = default_is_stmt
        self.line_base = line_base
        self.line_range = line_range
        self.opcode_base = opcode_base
        self.std_opcode_lengths = std_opcode_lengths
        self.directories = directories
        self.file_names = file_names
        self.prog = prog

    @classmethod
    def parse(cls, dwarf, stream):
        offset = stream.tell()
        unit_length = endian_read(stream, dwarf.elf_file.endian, 4)
        if unit_length == 0xFFFFFFFF:
            unit_length = endian_read(stream, dwarf.elf_file.endian, 8)
            unit_length_size = 8
            arch = ARCH.ARCH_64
        else:
            unit_length_size = 4
            arch = ARCH.ARCH_32
        version = endian_read(stream, dwarf.elf_file.endian, 2)
        if version != 5:
            raise DWARFError(
                f"can't read line header: only version 5 is currently supported ({version=})"
            )
        addr_size, segment_sel_size = read_struct(stream, "BB")

        # a dumb way to pass metadata to the form parser.
        # the reason i don't pass an actual cu is because of the ominous comments in the dwarf documentation
        # about how it's "common practice" to remove everything but the line info
        # XXX: this is only temporary
        # TODO: replace with a more robust system before merging (dataclass?)

        dummycu = CompilationUnit(
            0, arch, 5, None, 0, addr_size, None, b"", dwarf, None, 0, 0, 0, 0
        )
        header_length = endian_read(stream, dwarf.elf_file.endian, unit_length_size)
        prog_offset = stream.tell() - offset + header_length
        prog_size = unit_length - prog_offset + unit_length_size  # right??
        print(prog_size, unit_length, prog_offset + prog_size)
        (
            min_instr_length,
            max_op_per_instr,
            default_is_stmt,
            line_base,
            line_range,
            opcode_base,
        ) = read_struct(stream, "BBBbBB")
        std_opcode_lengths = read_struct(stream, f"{opcode_base-1}B")
        directories = _read_formatted(stream, dummycu)
        file_names = _read_formatted(stream, dummycu)
        state = State(bool(default_is_stmt), file_names)
        prog_end = stream.tell() + prog_size
        while stream.tell() < prog_end:
            instr = ProgramInstr.parse(
                stream,
                std_opcode_lengths,
                opcode_base,
                line_base,
                line_range,
                state,
                min_instr_length,
                max_op_per_instr,
                dwarf,
            )
            instr.execute(state, min_instr_length, max_op_per_instr)
        return cls(
            unit_length,
            arch,
            version,
            addr_size,
            segment_sel_size,
            dummycu,
            min_instr_length,
            max_op_per_instr,
            default_is_stmt,
            line_base,
            line_range,
            opcode_base,
            std_opcode_lengths,
            directories,
            file_names,
            state.matrix,
        )
