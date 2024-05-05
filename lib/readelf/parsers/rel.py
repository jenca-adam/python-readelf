import io
from ..helpers import endian_read
from ..const import *
class RelEntry:
    def __init__(self,offset, info, arch):
        self.offset=offset
        self.info=info
        if arch==Arch.ARCH_32:
            self.sym=self.info>>8
            self.type=self.info&0xff
        else:
            self.sym=self.info>>32
            self.type=self.info&0xffffffff

class Rel:
    def __init__(self, content, file):
        self.arch=self.file.arch
        self.stream = io.BytesIO(content)
        self.entries = []
        while self.stream.tell()<len(self.content)-1:
            if self.arch==Arch.ARCH_32:
                offset=endian_read(self.stream,file.endian,4)
                info=endian_read(self.stream, file.endian, 4)
            else:
                offset=endian_read(self.stream, file.endian, 8)
                info=endian_read(self.stream, file.endian, 8)
            self.entries.append(RelEntry(offset, info, self.arch))

