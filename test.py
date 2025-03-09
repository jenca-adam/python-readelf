import readelf
import pprint

pp = readelf.readelf("tests/renderer")
dw = pp.get_dwarf()
pprint.pprint(dw.lnos[0].prog)
# dies = [list(u.get_dies()) for u in dw.units]
