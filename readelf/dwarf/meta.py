from dataclasses import dataclass
from readelf.const import ARCH, ENDIAN
from .die import DIEPtr


@dataclass
class DWARFMeta:
    arch: ARCH
    endian: ENDIAN
    addr_size: int
    dwarf: object
    version: int = 5
    _dieptrclass: type = DIEPtr
