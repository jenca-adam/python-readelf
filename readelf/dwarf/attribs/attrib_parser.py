from .form import parse_form
from .lang import parse_lang
from .as_int import parse_as_int
from readelf.const import DW_AT

ATTRIB_PARSER_MAPPING = {
    DW_AT.DW_AT_language: parse_lang,
    DW_AT.DW_AT_low_pc: parse_as_int,
    DW_AT.DW_AT_high_pc: parse_as_int,
}


def parse_attrib(attr, form, stream, cu):
    form, supp = form
    form_parsed = parse_form(form, stream, cu, supp)
    parser = ATTRIB_PARSER_MAPPING.get(attr)
    if parser is None:
        return form_parsed
    return parser(form_parsed, cu)
