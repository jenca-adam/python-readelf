from readelf.const import DW_AT, DW_TAG
import math


class StructureType:
    def __init__(self, die):
        attrs = die.attrs
        self.name = attrs.get(DW_AT.DW_AT_name)
        self.export_symbols = attrs.get(DW_AT.DW_AT_export_symbols)
        self.byte_size = attrs.get(DW_AT.DW_AT_byte_size)
        self.bit_size = attrs.get(DW_AT.DW_AT_bit_size)
        self.struct_size = (
            self.byte_size or math.ceil(self.bit_size / 8) if self.bit_size else None
        )
        self.declaration = attrs.get(DW_AT.DW_AT_declaration)
        self.specification = attrs.get(DW_AT.DW_AT_specification)
        self.signature = attrs.get(DW_AT.DW_AT_signature)
        self._die = die
        # self.member_size = sum(m.member_size for m in self.members)

    def members(self):
        return [chld for chld in self._die.children if chld.tag == DW_TAG.DW_TAG_member]

    def decode(self, stream):
        st = {}
        for member in self.members():
            data = member.type.decode(stream)
            st[member.name] = data
        return st


class ClassType(StructureType):
    pass


class UnionType(StructureType):
    pass
