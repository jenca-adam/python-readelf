import readelf

pp = readelf.readelf("tests/renderer")
dw = pp.get_dwarf()
dies = list(dw.units[1].get_dies())
