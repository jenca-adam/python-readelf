import io


class Section:
    def __init__(self, sec_dict, sections, buf):
        self.sections = sections
        self.sec_dict = sec_dict
        self.flags = sec_dict["flags"]
        self.type = sec_dict["type"]
        self.addr = sec_dict["addr"]
        self.offset = sec_dict["offset"]
        self.size = sec_dict["size"]
        self.link = sec_dict["link"]
        self.info = sec_dict["info"]
        self.addralign = sec_dict["addralign"]
        self.entsize = sec_dict["entsize"]
        buf.seek(self.offset)
        self.content = buf.read(self.size)

    def __repr__(self):
        return f"<Section {self.name} @ {self.addr:#x}>"

    @property
    def name(self):
        return self.sections.strtab.get_name(self.sec_dict["name"])


class StringTable:
    def __init__(self, content):
        self.content = content
        self.stream = io.BytesIO(self.content)

    def get_name(self, offset):
        self.stream.seek(offset)
        result = bytearray()
        while True:
            nb = self.stream.read(1)
            if nb == b"\x00" or not nb:
                break
            result.append(ord(nb))
        self.stream.seek(0)
        return bytes(result).decode("ascii")
