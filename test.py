import readelf

pp = readelf.readelf("tests/renderer")
dw = pp.get_dwarf()
dies = [list(u.get_dies()) for u in dw.units]
