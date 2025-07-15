from readelf.const import DW_AT


class Typedef:
    def __init__(self, die):
        attrs = die.attrs
        type_ref = attrs.get(DW_AT.DW_AT_type)
        self.name = attrs.get(DW_AT.DW_AT_name)
        self.type = type_ref.content if type_ref else None

    def decode(self, stream):
        if self.type is None:
            raise ValueError("no type assigned")
        return self.type.decode(stream)
