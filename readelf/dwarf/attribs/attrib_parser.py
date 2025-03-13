from .form import parse_form
from .enum import make_enum_parser
from .as_int import parse_as_int
from readelf.const import DW_AT, DW_LANG, DW_ATE, DW_END

ATTRIB_PARSER_MAPPING = {
    DW_AT.DW_AT_language: make_enum_parser(
        DW_LANG, "DW_LANG_lo_user", "DW_LANG_hi_user"
    ),
    DW_AT.DW_AT_encoding: make_enum_parser(DW_ATE, "DW_ATE_lo_user", "DW_ATE_hi_user"),
    DW_AT.DW_AT_endianity: make_enum_parser(DW_END, "DW_END_lo_user", "DW_END_hi_user"),
    DW_AT.DW_AT_byte_size: parse_as_int,
    DW_AT.DW_AT_bit_size: parse_as_int,
    DW_AT.DW_AT_data_bit_offset: parse_as_int,
    DW_AT.DW_AT_low_pc: parse_as_int,
    DW_AT.DW_AT_high_pc: parse_as_int,
}


def parse_attrib(attr, form, stream, meta):
    form, supp = form
    form_parsed = parse_form(form, stream, meta, supp)
    parser = ATTRIB_PARSER_MAPPING.get(attr)
    if parser is None:
        return form_parsed
    return parser(form_parsed, meta)
