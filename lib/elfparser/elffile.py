from .header import parse_header, parse_section_header, parse_program_header
from .const import *
from .err import *
from .sections import Section, StringTable
from .segments import ProgramSegments


class ELFFile:
    def __init__(self, sec_dicts, buf, meta, sh_str_index=None):
        self.sec_dicts = sec_dicts
        self.meta = meta
        self.__dict__.update(self.meta)
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
        ph_entries = parse_program_header(
            self.buf,
            self.meta["phoff"],
            self.meta["phentsize"],
            self.meta["phnum"],
            self.meta["endian"],
            self.meta["arch"],
        )
        self.segments = ProgramSegments(ph_entries, self.buf, self)
        self.close()
    def __getitem__(self, i):
        return self.segments[i]
    
    def find_section(self, name):
        return tuple(q for q in self.sections if q.name == name)

    def find_at_offset(self, offset):
        for section in self.sections:
            if section.offset == offset:
                return section
        raise LookupError(f"No section found at offset {offset}")

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

    def close(self):
        self.buf.close()


def elfopen(fname):
    return ELFFile.from_stream(open(fname, "rb"))
