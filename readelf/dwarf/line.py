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


class ProgramInstr:
    def __init__(self, typ, operands):
        self.typ = typ
        self.operands = operands

    @classmethod
    def parse(self, stream, std_opcode_lengths, opcode_base):
        opcode = read_struct(stream, "B")
        if opcode == 0:
            ext_opcode = read_struct(stream, "B")
            typ = DW_LNE(ext_opcode)


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

        # a dumb way to pass metadata to form parser.
        # the reason i don't pass a cu is because of the ominous comments in the dwarf documentation
        # about how it's "common practice" to remove everything but the line info
        # XXX: this is only temporary
        # TODO: replace with a more robust system before merging (dataclass)

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

        prog = stream.read(prog_size)
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
