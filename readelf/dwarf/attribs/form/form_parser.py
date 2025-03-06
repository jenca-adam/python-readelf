from readelf.const import DW_FORM
from .strp import parse_strp, parse_line_strp, parse_strp_sup
from .const import (
    parse_data1,
    parse_data2,
    parse_data4,
    parse_data8,
    parse_udata,
    parse_sdata,
    parse_implicit_const,
)
from .addr import parse_addr
FORM_TO_PARSER_MAPPING = {
    DW_FORM.DW_FORM_strp: parse_strp,
    DW_FORM.DW_FORM_line_strp: parse_line_strp,
    DW_FORM.DW_FORM_strp_sup: parse_strp_sup,
    DW_FORM.DW_FORM_data1: parse_data1,
    DW_FORM.DW_FORM_data2: parse_data2,
    DW_FORM.DW_FORM_data4: parse_data4,
    DW_FORM.DW_FORM_data8: parse_data8,
    DW_FORM.DW_FORM_sdata: parse_sdata,
    DW_FORM.DW_FORM_udata: parse_udata,
    DW_FORM.DW_FORM_implicit_const: parse_implicit_const,
    DW_FORM.DW_FORM_addr: parse_addr
}


def parse_form(form, stream, cu, supp):
    parser = FORM_TO_PARSER_MAPPING.get(form)
    if parser is None:
        return None
    return parser(stream, cu, supp)
