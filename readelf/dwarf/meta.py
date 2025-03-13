from dataclasses import dataclass
from readelf.const import ARCH, ENDIAN
@dataclass
class DWARFMeta:
    arch: ARCH
    endian: ENDIAN
    addr_size: int
    dwarf: object 
    version: int = 5
