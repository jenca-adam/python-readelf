from .const import parse_data1, parse_data2, parse_data4, parse_data8, parse_udata
from .sec_offset import parse_sec_offset
from ..as_int import parse_as_int
import io


def make_dieptr(meta, off):
    return meta._dieptrclass(meta, off, False)


def parse_ref1(stream, meta, supp):
    return make_dieptr(
        meta,
        parse_as_int(
            parse_data1(stream, meta, supp),
            meta,
        ),
    )


def parse_ref2(stream, meta, supp):
    return make_dieptr(
        meta,
        parse_as_int(
            parse_data2(stream, meta, supp),
            meta,
        ),
    )


def parse_ref4(stream, meta, supp):
    return make_dieptr(
        meta,
        parse_as_int(
            parse_data4(stream, meta, supp),
            meta,
        ),
    )


def parse_ref8(stream, meta, supp):
    return make_dieptr(
        meta,
        parse_as_int(
            parse_data8(stream, meta, supp),
            meta,
        ),
    )


def parse_ref_udata(stream, meta, supp):
    return make_dieptr(
        meta,
        parse_as_int(
            parse_udata(stream, meta, supp),
            meta,
        ),
    )


def parse_ref_addr(stream, meta, supp):
    offset_int = parse_sec_offset(stream, meta, supp)
    return meta._dieptrclass(meta, offset_int, True)
