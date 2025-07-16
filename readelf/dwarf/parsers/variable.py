from readelf.const import DW_AT


class Variable:
    def __init__(self, die):
        attrs = die.attrs
        self.name = attrs.get(DW_AT.DW_AT_name)
        self.external = attrs.get(DW_AT.DW_AT_external)
        self.declaration = attrs.get(DW_AT.DW_AT_declaration)
        self.location = attrs.get(DW_AT.DW_AT_location)
        type_ref = attrs.get(DW_AT.DW_AT_type)
        self.name = attrs.get(DW_AT.DW_AT_name)
        self.specification = attrs.get(DW_AT.DW_AT_specification)
        self.variable_parameter = attrs.get(DW_AT.DW_AT_variable_parameter)
        self.is_optional = attrs.get(DW_AT.DW_AT_is_optional)
        self.default_value = attrs.get(DW_AT.DW_AT_default_value)
        self.const_value = attrs.get(DW_AT.DW_AT_const_value)
        self.endianity = attrs.get(DW_AT.DW_AT_endianity)
        self.const_expr = attrs.get(DW_AT.DW_AT_const_expr)
        self.linkage_name = attrs.get(DW_AT.DW_AT_linkage_name)
        self.type = type_ref.content if type_ref else None


class Constant(Variable):
    pass


class FormalParameter(Variable):
    pass
