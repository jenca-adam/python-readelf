import io
from .parsers import parse_content
from .helpers import map_public_attributes


class Section:
    def __init__(self, sec_dict, sections, buf, is_str_tab=False):
        self.file = sections
        self.is_str_tab = is_str_tab
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
        self.parsed_content = parse_content(
            self.type, self.content, self.file, sec_dict
        )
        map_public_attributes(self.parsed_content, self)

    def __repr__(self):
        return f"<Section {self.name} @ {self.addr:#x}>"

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value

    @property
    def name(self):
        if self.is_str_tab:
            return ".shstrtab"
        return self.file.strtab.get_name(self.sec_dict["name"])
