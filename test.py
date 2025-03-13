import readelf
import pprint

pp = readelf.readelf("tests/renderer")
dw = pp.get_dwarf()
# for lnop in dw.lnos:
#    pprint.pprint(lnop.matrix)
dies = [list(u.get_dies()) for u in dw.units]
