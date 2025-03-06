from readelf.const import DW_LANG
from readelf.dwarf.err import DWARFError
from .as_int import parse_as_int


def parse_lang(form, cu):
    form = parse_as_int(form, cu)
    if DW_LANG.DW_LANG_lo_user.value <= form <= DW_LANG.DW_LANG_hi_user.value:
        return DW_LANG.DW_LANG_lo_user
    if form not in DW_LANG:
        raise DWARFError(f"invalid DW_LANG: {form}")
    return DW_LANG(form)
