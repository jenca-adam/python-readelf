from readelf.helpers import endian_parse


def parse_as_int(form, meta):
    print(form)
    if isinstance(form, bytes):
        form = endian_parse(form, meta.endian)
    elif not isinstance(form, int):
        raise TypeError(
            f"got invalid argument type, expected int or bytes, got {form.__class__.__name__}"
        )
    return form
