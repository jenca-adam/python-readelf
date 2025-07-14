from readelf.const import DW_AT


class Member:
    def __init__(self, die):
        attrs = die.attrs
        self.name = attrs.get(DW_AT.DW_AT_name)
        self.type = attrs[DW_AT.DW_AT_type].content
        self.accessibility = attrs.get(DW_AT.DW_AT_accessibility)
        self.mutable = attrs.get(DW_AT.DW_AT_mutable)
        self.member_location = attrs.get(DW_AT.DW_AT_data_member_location, 0)
        self.bit_offset = attrs.get(DW_AT.DW_AT_data_bit_offset, 0)
        self.member_size = getattr(self.type, "type_size", 0)
