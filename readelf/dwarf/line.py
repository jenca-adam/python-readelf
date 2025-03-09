from .err import DWARFError
from .leb128 import leb128_parse
from .attribs.form import parse_form
from .unit import CompilationUnit
from readelf.helpers import endian_read, read_struct
from readelf.const import DW_FORM, DW_LNCT, ARCH, DW_LNS, DW_LNE


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


class State:
    def __init__(self, default_is_stmt):
        self.address = 0
        self.op_index = 0
        self.file = 1
        self.line = 1
        self.column = 0
        self.is_stmt = default_is_stmt
        self.basic_block = False
        self.end_sequence = False
        self.prologue_end = False
        self.epilogue_begin = False
        self.isa = 0
        self.discriminator = 0
        self.matrix = []

    def append_matrix(self):
        pass


class Operation:
    def __init__(
        self,
        line_set=0,
        address_set=0,
        op_index_set=0,
        file_set=None,
        col_set=None,
        is_stmt_toggle=False,
        basic_block_set=None,
        end_sequence_set=None,
        prologue_end_set=None,
        epilogue_begin_set=None,
        isa_set=None,
        discriminator_set=None,
        append_matrix=False,
    ):
        self.line_set = line_set
        self.address_set = address_set
        self.op_index_set = op_index_set
        self.file_set = file_set
        self.col_set = col_set
        self.is_stmt_toggle = is_stmt_toggle
        self.basic_block_set = basic_block_set
        self.end_sequence_set = end_sequence_set
        self.prologue_end_set = prologue_end_set
        self.epilogue_begin_set = epilogue_begin_set
        self.isa_set = isa_set
        self.discriminator_set = discriminator_set
        self.append_matrix = append_matrix

    def execute(self, state):
        if self.line_set is not None:
            state.line = self.line_set
        if self.address_set is not None:
            state.address = self.address_set
        ## etc
        if self.op_index_set is not None:
            state.op_index = self.op_index_set
        if self.file_set is not None:
            state.file = self.file_set
        if self.col_set is not None:
            state.col = self.col_set
        if self.is_stmt_toggle:
            state.is_stmt = not state.is_stmt
        if self.basic_block_set is not None:
            state.basic_block_set = self.basic_block_set
        if self.end_sequence_set is not None:
            state.end_sequence = self.end_sequence_set
        if self.prologue_end_set is not None:
            state.prologue_end = self.prologue_end_set
        if self.epilogue_begin_set is not None:
            state.epilogue_begin = self.epilogue_begin_set
        if self.isa_set is not None:
            state.isa = self.isa_set
        if self.discriminator_set is not None:
            state.discriminator = self.discriminator_set
        if self.append_matrix:
            state.append_matrix()

    @classmethod
    def from_special_opcode(
        cls,
        state,
        opcode,
        opcode_base,
        line_base,
        line_range,
        minimum_instruction_length,
        maximum_operations_per_instruction,
    ):
        adjusted = opcode - opcode_base
        op_advance = adjusted // line_range
        line_increment = line_base + (adjusted % line_range)
        line_set = state.line + line_increment
        address_set = state.address + minimum_instruction_length * (
            (state.op_index + op_advance) // maximum_operations_per_instruction
        )
        op_index_set = (
            state.op_index + op_advance
        ) % maximum_operations_per_instruction
        return cls(
            line_set=line_set,
            address_set=address_set,
            op_index_set=op_index_set,
            basic_block_set=False,
            prologue_end_set=False,
            epilogue_begin_set=False,
            discriminator_set=0,
            append_matrix=True,
        )

    def __repr__(self):
        return f"Operation(line={self.line_set}, addr={self.address_set}, op_index={self.op_index_set})"


class ProgramInstr:
    def __init__(self, typ, operands):
        self.typ = typ
        self.operands = operands

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
    ):
        (opcode,) = read_struct(stream, "B")
        if opcode == 0:  # extended
            length = leb128_parse(stream)
            (ext_opcode,) = read_struct(stream, "B")
            typ = DW_LNE(ext_opcode)
            operands = stream.read(length - 1)
        elif opcode < opcode_base:
            typ = DW_LNS(opcode)
            n_ops = std_opcode_lengths[opcode - 1]
            operands = [leb128_parse(stream) for _ in range(n_ops)]
        else:
            typ = Operation.from_special_opcode(
                state,
                opcode,
                opcode_base,
                line_base,
                line_range,
                minimum_instruction_length,
                maximum_operations_per_instruction,
            )
            operands = None
        return cls(typ, operands)

    def __repr__(self):
        return (
            f"ProgramInstr({self.typ}{f', {self.operands}' if self.operands else ''})"
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
        state = State(bool(default_is_stmt))
        prog = []
        prog_end = stream.tell() + prog_size
        while stream.tell() < prog_end:
            prog.append(
                ProgramInstr.parse(
                    stream,
                    std_opcode_lengths,
                    opcode_base,
                    line_base,
                    line_range,
                    state,
                    min_instr_length,
                    max_op_per_instr,
                )
            )
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
            prog,
        )
