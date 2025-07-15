from .base_type import BaseType
from .struct import StructureType, UnionType, ClassType
from .member import Member
from .modified import ModifiedType
from .typedef import Typedef
from .array import Array
from .variable import Variable, Constant, FormalParameter
from readelf.const import DW_TAG


class NotSpecial:
    def __init__(self, *_):
        pass


TAG_TO_PARSER_MAPPING = {
    DW_TAG.DW_TAG_base_type: BaseType,
    DW_TAG.DW_TAG_structure_type: StructureType,
    DW_TAG.DW_TAG_union_type: UnionType,
    DW_TAG.DW_TAG_class_type: ClassType,
    DW_TAG.DW_TAG_member: Member,
    DW_TAG.DW_TAG_atomic_type: ModifiedType,
    DW_TAG.DW_TAG_const_type: ModifiedType,
    DW_TAG.DW_TAG_immutable_type: ModifiedType,
    DW_TAG.DW_TAG_packed_type: ModifiedType,
    DW_TAG.DW_TAG_pointer_type: ModifiedType,
    DW_TAG.DW_TAG_reference_type: ModifiedType,
    DW_TAG.DW_TAG_restrict_type: ModifiedType,
    DW_TAG.DW_TAG_rvalue_reference_type: ModifiedType,
    DW_TAG.DW_TAG_shared_type: ModifiedType,
    DW_TAG.DW_TAG_volatile_type: ModifiedType,
    DW_TAG.DW_TAG_typedef: Typedef,
    DW_TAG.DW_TAG_array_type: Array,
    DW_TAG.DW_TAG_variable: Variable,
    DW_TAG.DW_TAG_constant: Constant,
    DW_TAG.DW_TAG_formal_parameter: FormalParameter

}


def parse_die(die):
    return TAG_TO_PARSER_MAPPING.get(die.tag, NotSpecial)(die)
