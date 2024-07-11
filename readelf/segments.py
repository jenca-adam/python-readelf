class ProgramSegmentFlags:
    def __init__(self, flags):
        self.readable = flags & 0x1
        self.writable = flags & 0x2
        self.executable = flags & 0x4
        self.__string = "".join(
            (
                "r" if self.readable else "-",
                "w" if self.writable else "-",
                "x" if self.executable else "-",
            )
        )

    def __repr__(self):
        return f"<ProgramSegmentFlags {(self.__string)!r}>"


class ProgramSegment:
    def __init__(self, segment, buf, file):
        self.__dict__.update(segment)
        self.segment = segment
        self.file = file
        self.flags = ProgramSegmentFlags(segment["flags"])
        self.readable = self.flags.readable
        self.writable = self.flags.writable
        self.executable = self.flags.executable
        self.buf = buf
        self.content = self.load_content()
        self.sections = self.load_sections()

    def load_sections(self):
        sections = []
        for section in self.file.sections:
            if (
                self.segment["offset"] <= section.offset
                and section.offset + section.size
                <= self.segment["offset"] + self.segment["filesz"]
            ):
                sections.append(section)
        return sections

    def load_content(self):
        self.buf.seek(self.segment["offset"])
        return self.buf.read(self.segment["filesz"])

    def __getitem__(self, i):
        return self.sections[i]

    def __repr__(self):
        return f"<ProgramSegment ({self.flags}) {self.type}" + (
            f" containing {' '.join([sec.name for sec in self.sections])}>"
            if self.sections
            else ">"
        )


class ProgramSegments:
    def __init__(self, segments, buf, file):
        self.segments = [ProgramSegment(seg, buf, file) for seg in segments]
        self.buf = buf
        self.file = file

    def __getitem__(self, i):
        return self.segments[i]

    def __repr__(self):
        return f"<ProgramSegments {repr(self.segments)}>"
