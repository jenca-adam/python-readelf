from readelf.const import DW_FORM
from .strp import parse_strp, parse_line_strp, parse_strp_sup
from .string import parse_string
from .const import (
    parse_data1,
    parse_data2,
    parse_data4,
    parse_data8,
    parse_udata,
    parse_sdata,
    parse_implicit_const,
)
from .ref import (
    parse_ref1,
    parse_ref2,
    parse_ref4,
    parse_ref8,
    parse_ref_udata,
    parse_ref_addr,
)

from .addr import parse_addr
from .sec_offset import parse_sec_offset
from .flag import parse_flag, parse_flag_present

FORM_TO_PARSER_MAPPING = {
    DW_FORM.DW_FORM_strp: parse_strp,
    DW_FORM.DW_FORM_line_strp: parse_line_strp,
    DW_FORM.DW_FORM_strp_sup: parse_strp_sup,
    DW_FORM.DW_FORM_string: parse_string,
    DW_FORM.DW_FORM_data1: parse_data1,
    DW_FORM.DW_FORM_data2: parse_data2,
    DW_FORM.DW_FORM_data4: parse_data4,
    DW_FORM.DW_FORM_data8: parse_data8,
    DW_FORM.DW_FORM_sdata: parse_sdata,
    DW_FORM.DW_FORM_udata: parse_udata,
    DW_FORM.DW_FORM_implicit_const: parse_implicit_const,
    DW_FORM.DW_FORM_addr: parse_addr,
    DW_FORM.DW_FORM_sec_offset: parse_sec_offset,
    DW_FORM.DW_FORM_ref1: parse_ref1,
    DW_FORM.DW_FORM_ref2: parse_ref2,
    DW_FORM.DW_FORM_ref4: parse_ref4,
    DW_FORM.DW_FORM_ref8: parse_ref8,
    DW_FORM.DW_FORM_ref_udata: parse_ref_udata,
    DW_FORM.DW_FORM_ref_addr: parse_ref_addr,
    DW_FORM.DW_FORM_flag: parse_flag,
    DW_FORM.DW_FORM_flag_present: parse_flag_present,
}


def parse_form(form, stream, cu, supp):
    parser = FORM_TO_PARSER_MAPPING.get(form)
    if parser is None:
        raise TypeError(form)
    return parser(stream, cu, supp)
