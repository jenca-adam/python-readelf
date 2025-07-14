from readelf.const import DW_AT, DW_TAG


class ModifiedType:
    def __init__(self, die):
        attrs = die.attrs
        self.tag = die.tag
        type_ref = attrs.get(DW_AT.DW_AT_type)
        self.name = attrs.get(DW_AT.DW_AT_name)
        self.type = type_ref.content if type_ref else None

    def decode(self, stream):
        if self.type is None:
            raise ValueError("no type assigned")
        if self.tag in (
            DW_TAG_atomic_type,
            DW_TAG_const_type,
            DW_TAG_immutable_type,
            DW_TAG_packed_type,
            DW_TAG_shared_type,
            DW_TAG_volatile_type,
        ):
            return self.type.decode(stream)
        raise NotImplementedError(f"decoding of {self.tag} not yet supported")
