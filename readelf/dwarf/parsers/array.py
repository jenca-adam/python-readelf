from readelf.const import DW_AT

class Array:
    def __init__(self, die):
        attrs = die.attrs
        self.name = attrs.get(DW_AT.DW_AT_name)
        self.ordering = attrs.get(DW_AT.DW_AT_ordering)
        self.type = attrs[DW_AT.DW_AT_type].content
        self.byte_stride = attrs.get(DW_AT.DW_AT_byte_stride)
        self.bit_stride = attrs.get(DW_AT.DW_AT_bit_stride)
        self.rank = attrs.get(DW_AT.DW_AT_rank)
        
