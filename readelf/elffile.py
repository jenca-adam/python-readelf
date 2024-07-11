from .header import parse_header, parse_section_header, parse_program_header
from .const import *
from .err import *
from .helpers import split_array
from .sections import Section
from .segments import ProgramSegments
from .memory import Memory


class ELFFile:
    def __init__(self, sec_dicts, buf, meta, sh_str_index=None):
        self.sec_dicts = sec_dicts
        self.meta = meta
        self.__dict__.update(self.meta)
        self.address_size = 8 if self.arch == ARCH.ARCH_64 else 4
        self.sections = []
        self.buf = buf

        self.memory = Memory()
        if sh_str_index is None:
            self.strtab = None

            for sec_d in sec_dicts:
                sec = Section(sec_d, self, self.buf)
                if sec.type == SHT.SHT_STRTAB:
                    self.strtab = Section(sec_d, self, self.buf, is_str_tab=True)
                self.sections.append(sec)
            if self.strtab is None:
                raise ParseError(".shstrtab section missing.")
        else:
            self.strtab = Section(
                sec_dicts[sh_str_index], self, self.buf, is_str_tab=True
            )
            self.sections = [
                Section(sec_d, self, self.buf, is_str_tab=False)
                for sec_d in self.sec_dicts
            ]
        ph_entries = parse_program_header(
            self.buf,
            self.meta["phoff"],
            self.meta["phentsize"],
            self.meta["phnum"],
            self.meta["endian"],
            self.meta["arch"],
        )
        self.segments = ProgramSegments(ph_entries, self.buf, self)
        for section in self.sections:
            if SHF.SHF_ALLOC in section.flags:
                self.memory.alloc(section.addr, section)
            if hasattr(section, "_after_init"):
                section._after_init()
        self.close()

    def __getitem__(self, i):
        return self.segments[i]

    def find_sections(self, name):
        return tuple(q for q in self.sections if q.name == name)

    def find_section(self, name):
        sec = self.find_sections(name)
        if not sec:
            raise LookupError(f"No {name} section found")
        return sec[0]

    def find_sections_by_type(self, sectype):
        return tuple(q for q in self.sections if q.type == sectype)

    def find_section_by_type(self, sectype):
        sec = self.find_sections_by_type(sectype)
        if not sec:
            raise LookupError(f"No section with the type {sectype} found")
        return sec[0]

    def _split_array(self, data):
        return split_array(data, self.address_size, self.endian)

    def find_at_offset(self, offset):
        for section in self.sections:
            if section.offset == offset:
                return section
        raise LookupError(f"No section found at offset {offset:x}")

    def find_at_addr(self, addr):
        for section in self.sections:
            if section.addr == addr:
                return section
        raise LookupError(f"No section found at address {addr:x}")

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


def readelf(fname):
    return ELFFile.from_stream(open(fname, "rb"))
