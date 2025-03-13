from readelf.helpers import read_struct, endian_read
from readelf.const import DW_FORM, DW_MACRO
from .leb128 import leb128_parse
from .attribs.form import parse_form
from .err import DWARFError

OPCODE_OPERANDS_TABLE = {
    DW_MACRO.DW_MACRO_define: (DW_FORM.DW_FORM_udata, DW_FORM.DW_FORM_string),
    DW_MACRO.DW_MACRO_undef: (DW_FORM.DW_FORM_udata, DW_FORM.DW_FORM_string),
    DW_MACRO.DW_MACRO_define_strp: (DW_FORM.DW_FORM_udata, DW_FORM.DW_FORM_strp),
    DW_MACRO.DW_MACRO_undef_strp: (DW_FORM.DW_FORM_udata, DW_FORM.DW_FORM_strp),
    DW_MACRO.DW_MACRO_start_file: (DW_FORM.DW_FORM_udata, DW_FORM.DW_FORM_data1),
    DW_MACRO.DW_MACRO_end_file: (),
    DW_MACRO.DW_MACRO_import: (DW_FORM.DW_FORM_sec_offset,),
    DW_MACRO.DW_MACRO_null: (),
}


class MacroUnitFlags:
    def __init__(self, flags):
        self.offset_size_flag = flags & 0x1
        self.debug_line_offset_flag = flags & 0x2
        self.opcode_operands_table_flag = flags & 0x4
        self.offset_size = self.offset_size_flag * 4 + 4


class Macro:
    def __init__(self, opcode, operands, file, **kwargs):
        self.opcode = opcode
        self.operands = operands
        self.file = file
        print(self)
        self.__dict__.update(kwargs)

    @classmethod
    def parse(cls, stream, opcode_operands_table, cu, dwarf, lnop, file_stack):
        opcode = DW_MACRO(read_struct(stream, "B")[0])
        operands = [
            parse_form(form, stream, cu, None) for form in opcode_operands_table[opcode]
        ]
        if opcode == DW_MACRO.DW_MACRO_null:
            yield False
            return
        else:
            yield True
        if opcode == DW_MACRO.DW_MACRO_import:
            operands[0] = MacroUnitPtr(
                stream, operands[0], dwarf, cu, lnop, file_stack.copy()
            )
        elif opcode == DW_MACRO.DW_MACRO_start_file and lnop:
            try:
                file = lnop.files[operands[1]]
            except:
                file = None
            file_stack.append(file)
        if opcode == DW_MACRO.DW_MACRO_end_file and file_stack:
            file = file_stack[-1]
            file_stack.pop()
        elif file_stack:
            file = file_stack[-1]
        else:
            file = None
        yield cls(opcode, operands, file)

    def __repr__(self):
        return f"<Macro {self.opcode} {self.operands} {self.file}>"


class MacroUnitPtr:
    def __init__(self, stream, offset, dwarf, cu, lnop, file_stack):
        self.stream = stream
        self.offset = offset
        self.dwarf = dwarf
        self.cu = cu
        self.lnop = lnop
        self.file_stack = file_stack
        self._content = None

    @property
    def content(self):
        if self._content is None:
            old_offset = self.stream.tell()
            self.stream.seek(self.offset)
            self._content = MacroUnit.parse(
                self.dwarf, self.stream, self.cu, self.lnop, self.file_stack
            )
            self.stream.seek(old_offset)
        return self._content

    def __repr__(self):
        return f"<MacroUnitPtr {self.offset:#x}>"


class MacroUnit:
    def __init__(self, macros, debug_line_offset, opcode_operands_table):
        self.macros = macros
        self.debug_line_offset = debug_line_offset
        self.opcode_operands_table = opcode_operands_table

    @classmethod
    def parse(cls, dwarf, stream, cu, lnop, file_stack=None):
        if file_stack is None:
            file_stack = []

        (version,) = read_struct(stream, "H", dwarf.elf_file.endian)
        if version != 5:
            raise DWARFError(
                f"can't read macro unit header: only version 5 is currently supported ({version=})"
            )

        flags = MacroUnitFlags(read_struct(stream, "B")[0])
        if flags.debug_line_offset_flag:
            debug_line_offset = endian_read(
                stream, dwarf.elf_file.endian, flags.offset_size
            )
        else:
            debug_line_offset = None

        opcode_operands_table = OPCODE_OPERANDS_TABLE
        if flags.opcode_operands_table_flag:
            (count,) = read_struct(stream, "B")
            for i in range(count):
                opcode = DW_MACRO(read_struct(stream, "B")[0])
                num_operands = leb128_parse(stream)
                operand_forms = [
                    DW_FORM(i) for i in read_struct(stream, f"{num_operands}B")
                ]
                opcode_operands_table[opcode] = operand_forms
        macros = []
        while True:
            gen = Macro.parse(
                stream, opcode_operands_table, cu, dwarf, lnop, file_stack
            )
            if not next(gen):
                break
            macros.extend(gen)
        return cls(macros, debug_line_offset, opcode_operands_table)
