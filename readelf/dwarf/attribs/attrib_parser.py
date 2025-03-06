from .form import parse_form


def parse_attrib(attr, form, stream, cu):
    form, supp = form
    return parse_form(form, stream, cu, supp)
