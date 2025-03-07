from .base_type import BaseType
from readelf.const import DW_TAG


class NotSpecial:
    def __init__(self, *_):
        pass


TAG_TO_PARSER_MAPPING = {DW_TAG.DW_TAG_base_type: BaseType}


def parse_die(die):
    return TAG_TO_PARSER_MAPPING.get(die.tag, NotSpecial)(die)
