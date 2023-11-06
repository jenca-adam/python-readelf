import io
from ..parsers.header import parse_header, parse_section_header
from ..const import *
from ..err import *


class Section:
    def __init__(self, sec_dict, sections, buf):
        self.sections = sections
        self.sec_dict = sec_dict
        self.flags = sec_dict["flags"]
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
        return f"<Section {self.name} @ {self.addr:#x} [{self.sec_dict}]>"

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
        return result


class Sections:
    def __init__(self, sec_dicts, buf, file, sh_str_index=None):
        self.sec_dicts = sec_dicts
        self.file = file  # TODO
        self.sections = []
        self.buf = buf
        if sh_str_index is None:
            self.strtab = None

            for sec_d in sec_dicts:
                sec = Section(sec_d, self, self.buf)
                if sec.type == SHT_STRTAB:
                    self.strtab = StringTable(sec.content)
                self.sections.append(sec)
            if self.strtab is None:
                raise ParseError(".shstrtab section missing.")
        else:
            self.strtab = StringTable(
                Section(sec_dicts[sh_str_index], self, self.buf).content
            )
            self.sections = [Section(sec_d, self, self.buf) for sec_d in self.sec_dicts]

    @classmethod
    def from_stream(cls, buf):
        meta = parse_header(buf)
        shargs = (
            meta["shoff"],
            meta["shentsize"],
            meta["shnum"],
            meta["endian"],
            meta["arch"],
        )  # section header specific stuff
        sh_str_index = meta["shstrndx"]
        sec_dicts = parse_section_header(buf, *shargs)
        return cls(sec_dicts, buf, meta, sh_str_index)
