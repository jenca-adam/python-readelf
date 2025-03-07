from readelf.const import DW_AT, DW_ATE, DW_END, ENDIAN
from readelf.dwarf.err import DWARFError, DWARFEncodingError
from readelf.helpers import endian_parse
import math
import struct

STRUCTS = {
    (DW_ATE.DW_ATE_boolean, 1): "?",
    (DW_ATE.DW_ATE_signed_char, 1): "b",
    (DW_ATE.DW_ATE_unsigned_char, 1): "B",
    (DW_ATE.DW_ATE_signed, 1): "b",
    (DW_ATE.DW_ATE_signed, 2): "h",
    (DW_ATE.DW_ATE_signed, 4): "i",
    (DW_ATE.DW_ATE_signed, 8): "q",
    (DW_ATE.DW_ATE_unsigned, 1): "B",
    (DW_ATE.DW_ATE_unsigned, 2): "H",
    (DW_ATE.DW_ATE_unsigned, 4): "I",
    (DW_ATE.DW_ATE_unsigned, 8): "Q",
    (DW_ATE.DW_ATE_float, 2): "e",
    (DW_ATE.DW_ATE_float, 4): "f",
    (DW_ATE.DW_ATE_float, 8): "d",
    (DW_ATE.DW_ATE_imaginary_float, 2): "e",
    (DW_ATE.DW_ATE_imaginary_float, 4): "f",
    (DW_ATE.DW_ATE_imaginary_float, 8): "d",
}

ENDIANS = {
    DW_END.DW_END_little: "<",
    DW_END.DW_END_big: ">",
}


class BaseType:
    def __init__(self, die):
        attrs = die.attrs

        self.encoding = attrs.get(DW_AT.DW_AT_encoding)
        self.endianity = attrs.get(DW_AT.DW_AT_endianity) or DW_END.from_endian(
            die.cu.parent.elf_file.endian
        )
        self._byte_size = attrs.get(DW_AT.DW_AT_byte_size)
        self.bit_size = attrs.get(DW_AT.DW_AT_bit_size)
        self.data_bit_offset = attrs.get(DW_AT.DW_AT_data_bit_offset, 0)
        self.digit_count = attrs.get(DW_AT.DW_AT_digit_count)
        self.name = attrs.get(DW_AT.DW_AT_name)

        if not self.encoding:
            raise DWARFError("base_type missing required attribute encoding")
        if self._byte_size is None and self.bit_size is None:
            raise DWARFError(
                "base_type must have either byte_size or bit_size attributes"
            )
        if self._byte_size is not None:
            self.type_size = self._byte_size
        else:
            self.type_size = math.ceil((self.bit_size + self.data_bit_offset) / 8)

        self.struct_string = STRUCTS.get((self.encoding, self.type_size))
        if self.struct_string is not None:
            _endian_string = ENDIANS[self.endianity]
            self.struct_string = _endian_string + self.struct_string

    def decode(self, stream):
        buf = stream.read(self.type_size)
        if self.struct_string is not None:
            return struct.unpack(self.struct_string, buf)[0]
        elif (
            self.encoding == DW_ATE.DW_ATE_unsigned
            and self.type_size == self._byte_size
        ):  # not sure how to handle bits for now
            return endian_parse(buf, ENDIAN.from_dw_end(self.endianity))
        elif (
            self.encoding == DW_ATE.DW_ATE_signed and self.type_size == self._byte_size
        ):
            i = endian_parse(buf, ENDIAN.from_dw_end(self.endianity))
            sb_mask = 1 << self.type_size
            sign_bit, value = (i & sb_mask) >> self.type_size, i & ~sb_mask
            return value * (-1) ** sign_bit
        elif self.encoding == DW_ATE.DW_ATE_ASCII:
            return buf.decode("ascii")
        elif self.encoding == DW_ATE.DW_ATE_UTF:
            return buf.decode("utf-8")
        elif self.encoding == DW_ATE.DW_ATE_complex_float:
            sfmt = STRUCTS.get((DW_ATE.DW_ATE_float, self.type_size // 2))
            if sfmt:
                return complex(*struct.unpack(sfmt * 2, buf))
