from readelf.const import DW_FORM
from .strp import make_strp_parser

FORM_TO_PARSER_MAPPING = {DW_FORM.DW_FORM_strp: make_strp_parser(".debug_str")}


def parse_attrib(form_suppl, stream, cu):
    form, suppl = form_suppl
    parser = FORM_TO_PARSER_MAPPING.get(form)
    if parser is None:
        return None
    return parser(stream, cu)
