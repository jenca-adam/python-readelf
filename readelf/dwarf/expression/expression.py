from readelf.const import DW_OP
from readelf.helpers import read_struct, endian_read
from readelf.dwarf.leb128 import leb128_parse
from readelf.dwarf.parsers.base_type import BaseType
from readelf.dwarf.err import DWARFError

STRUCTS = {
    DW_OP.DW_OP_const1u: "B",
    DW_OP.DW_OP_const2u: "H",
    DW_OP.DW_OP_const4u: "I",
    DW_OP.DW_OP_const8u: "L",
    DW_OP.DW_OP_const1u: "b",
    DW_OP.DW_OP_const2u: "h",
    DW_OP.DW_OP_const4u: "i",
    DW_OP.DW_OP_const8u: "l",
}



class Expression:
    pass
def get_operands(op, cu, stream, meta):
    if DW_OP.DW_OP_lit0 <= op.value <= DW_OP.DW_OP_lit31:
        return [op.value - DW_OP.DW_OP_lit0.value]
    elif op == DW_OP.DW_OP_addr:
        return [endian_read(stream, meta.endian, meta.addr_size)]
    elif op in STRUCTS:
        return [read_struct(stream, STRUCTS[op], meta.endian)]
    elif op == DW_OP.DW_OP_constu:
        return [leb128_parse(stream)]
    elif op == DW_OP.DW_OP_consts:
        return [leb128_parse(stream, True)]
    elif op in (DW_OP.DW_OP_addrx, DW_OP.DW_OP_constx):
        if not cu.dwarf.address_tables:
            raise DWARFError(f"{op} without address tables")
        offset = leb128_parse(stream)
        
    elif op == DW_OP.DW_OP_const_type:
        die_offset = leb128_parse(stream)
        die = cu.die_at_offset(die_offset)
        (size,) = read_struct(stream, "B")
        return die.decode(endian_read(stream, meta.endian, size))
