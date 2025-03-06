from .const import parse_data1, parse_data2, parse_data4, parse_data8, parse_udata
from .sec_offset import parse_sec_offset
from ..as_int import parse_as_int
import io


def make_dieptr(cu, off):
    return cu._dieptrclass(cu, off, False)


def parse_ref1(stream, cu, supp):
    return make_dieptr(
        cu,
        parse_as_int(
            parse_data1(stream, cu, supp),
            cu,
        ),
    )


def parse_ref2(stream, cu, supp):
    return make_dieptr(
        cu,
        parse_as_int(
            parse_data2(stream, cu, supp),
            cu,
        ),
    )


def parse_ref4(stream, cu, supp):
    return make_dieptr(
        cu,
        parse_as_int(
            parse_data4(stream, cu, supp),
            cu,
        ),
    )


def parse_ref8(stream, cu, supp):
    return make_dieptr(
        cu,
        parse_as_int(
            parse_data8(stream, cu, supp),
            cu,
        ),
    )


def parse_ref_udata(stream, cu, supp):
    return make_dieptr(
        cu,
        parse_as_int(
            parse_udata(stream, cu, supp),
            cu,
        ),
    )


def parse_ref_addr(stream, cu, supp):
    offset_int = parse_sec_offset(stream, cu, supp)
    return cu._dieptrclass(cu, offset_int, True)
