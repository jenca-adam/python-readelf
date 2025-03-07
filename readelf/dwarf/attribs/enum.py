from readelf.dwarf.err import DWARFError
from .as_int import parse_as_int


def make_enum_parser(enum, lo_user_name=None, hi_user_name=None):
    def parse_enum(form, cu):
        form = parse_as_int(form, cu)
        lo_user = getattr(enum, lo_user_name, None)
        hi_user = getattr(enum, hi_user_name, None)
        if lo_user and hi_user:
            if lo_user.value <= form <= hi_user.value:
                return lo_user
        if form not in enum:
            raise DWARFError(f"invalid DW_LANG: {form}")
        return enum(form)

    return parse_enum
