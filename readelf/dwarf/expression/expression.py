from readelf.const import DW_OP
from readelf.helpers import read_struct, endian_read, is_eof
from readelf.dwarf.leb128 import leb128_parse

STRUCTS = {
    DW_OP.DW_OP_const1u: "B",
    DW_OP.DW_OP_const2u: "H",
    DW_OP.DW_OP_const4u: "I",
    DW_OP.DW_OP_const8u: "L",
    DW_OP.DW_OP_const1s: "b",
    DW_OP.DW_OP_const2s: "h",
    DW_OP.DW_OP_const4s: "i",
    DW_OP.DW_OP_const8s: "l",
    DW_OP.DW_OP_pick: "B",
    DW_OP.DW_OP_deref_size: "B",
    DW_OP.DW_OP_xderef_size: "B",
    DW_OP.DW_OP_skip: "h",
    DW_OP.DW_OP_bra: "h",
    DW_OP.DW_OP_call2: "H",
    DW_OP.DW_OP_call4: "I",
}


class Operation:
    def __init__(self, type, operands):
        self.type = type
        self.operands = operands

    @classmethod
    def parse(cls, stream, cu, meta):
        (opcode,) = read_struct(stream, "B")
        op = DW_OP(opcode)
        print(op)
        operands = get_operands(op, cu, stream, meta)
        return cls(op, operands)

    def __repr__(self):
        return f"{self.type.name}({self.operands})"


class Expression:
    def __init__(self, operations):
        self.operations = operations

    def evaluate(self):
        # TODO
        raise NotImplementedError

    @classmethod
    def parse(cls, stream, cu, meta):
        operations = []
        while not is_eof(stream):
            operations.append(Operation.parse(stream, cu, meta))
        return cls(operations)

    def __repr__(self):
        return f"Expression({', '.join(repr(op) for op in self.operations)})"


def get_operands(op, cu, stream, meta):
    # parses a list of operands based on an opcode
    # for lit0-lit31, breg0-breg31, the list also includes the constant associated with the opcode
    # the operands are passed as integers(with the exception of DW_OP_entry_value), with no interpretation
    if DW_OP.DW_OP_lit0.value <= op.value <= DW_OP.DW_OP_lit31.value:
        return [op.value - DW_OP.DW_OP_lit0.value]
    elif op in (DW_OP.DW_OP_addr, DW_OP.DW_OP_call_ref):
        return [endian_read(stream, meta.endian, meta.addr_size)]
    elif op in STRUCTS:
        return [read_struct(stream, STRUCTS[op], meta.endian)]
    elif op == DW_OP.DW_OP_consts:
        return [leb128_parse(stream, True)]
    elif op in (
        DW_OP.DW_OP_constu,
        DW_OP.DW_OP_addrx,
        DW_OP.DW_OP_constx,
        DW_OP.DW_OP_fbreg,
        DW_OP.DW_OP_plus_uconst,
        DW_OP.DW_OP_convert,
        DW_OP.DW_OP_reinterpret,
        DW_OP.DW_OP_regx,
    ):
        return [leb128_parse(stream)]
    elif op == DW_OP.DW_OP_const_type:
        die_offset = leb128_parse(stream)
        (size,) = read_struct(stream, "B")
        return [die_offset, size, endian_read(stream, meta.endian, size)]
    elif DW_OP.DW_OP_breg0.value <= op.value <= DW_OP.DW_OP_breg31.value:
        return [op.value - DW_OP.DW_OP_breg0.value, leb128_parse(stream)]
    elif DW_OP.DW_OP_reg0.value <= op.value <= DW_OP.DW_OP_reg31.value:
        return [op.value - DW_OP.DW_OP_reg0.value]
    elif op in [DW_OP.DW_OP_bregx.value, DW_OP.DW_OP_regval_type.value]:
        return [leb128_parse(stream), leb128_parse(stream)]
    elif op in (
        DW_OP.DW_OP_dup,
        DW_OP.DW_OP_drop,
        DW_OP.DW_OP_over,
        DW_OP.DW_OP_swap,
        DW_OP.DW_OP_rot,
        DW_OP.DW_OP_deref,
        DW_OP.DW_OP_xderef,
        DW_OP.DW_OP_push_object_address,
        DW_OP.DW_OP_form_tls_address,
        DW_OP.DW_OP_call_frame_cfa,
        DW_OP.DW_OP_abs,
        DW_OP.DW_OP_and,
        DW_OP.DW_OP_div,
        DW_OP.DW_OP_minus,
        DW_OP.DW_OP_mod,
        DW_OP.DW_OP_mul,
        DW_OP.DW_OP_neg,
        DW_OP.DW_OP_not,
        DW_OP.DW_OP_or,
        DW_OP.DW_OP_plus,
        DW_OP.DW_OP_shl,
        DW_OP.DW_OP_shr,
        DW_OP.DW_OP_shra,
        DW_OP.DW_OP_xor,
        DW_OP.DW_OP_le,
        DW_OP.DW_OP_ge,
        DW_OP.DW_OP_eq,
        DW_OP.DW_OP_lt,
        DW_OP.DW_OP_gt,
        DW_OP.DW_OP_ne,
        DW_OP.DW_OP_nop,
        DW_OP.DW_OP_stack_value,
    ):
        return []
    elif op in (DW_OP.DW_OP_deref_type, DW_OP.DW_OP_xderef_type):
        return [read_struct(stream, "B"), leb128_parse(stream)]
    elif op in (DW_OP.DW_OP_entry_value, DW_OP.DW_OP_implicit_value):
        length = leb128_parse(stream)
        return [length, stream.read(length)]
    elif op == DW_OP.DW_OP_implicit_pointer:
        return [endian_read(stream, meta.endian, meta.addr_size), leb128_parse(stream)]
    else:
        raise NotImplementedError(f"unhandled operation: {op}")
