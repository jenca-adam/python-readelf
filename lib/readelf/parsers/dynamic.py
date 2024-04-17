from ..maps import DYNAMIC_TAG_MAP, DT_D_VAL, DT_D_PTR
from ..const import *
from ..helpers import endian_read
from io import BytesIO
import functools

###

DYN_INTERPRETERS = {}


def _add_dyn_interpreter(value):
    global DYN_INTERPRETERS

    def _add_dyn_interpreter_inner(func):
        DYN_INTERPRETERS[value] = func
        return func

    return _add_dyn_interpreter_inner


##


@_add_dyn_interpreter(DT_NEEDED)
@_add_dyn_interpreter(DT_SONAME)
@_add_dyn_interpreter(DT_RUNPATH)
@_add_dyn_interpreter(DT_AUXILIARY)
@_add_dyn_interpreter(DT_SUNW_AUXILIARY)
@_add_dyn_interpreter(DT_SUNW_FILTER)
def _dyn_interpret_in_dynstr(content, file, *_):
    dynstr = file.find_section(".dynstr")
    return dynstr.get_name(content)


@_add_dyn_interpreter(DT_INIT)
@_add_dyn_interpreter(DT_FINI)
@_add_dyn_interpreter(DT_STRTAB)
@_add_dyn_interpreter(DT_SYMTAB)
@_add_dyn_interpreter(DT_RELA)
@_add_dyn_interpreter(DT_VERNEED)
@_add_dyn_interpreter(DT_SUNW_CAP)
@_add_dyn_interpreter(DT_SYMINFO)
@_add_dyn_interpreter(DT_VERDEF)
@_add_dyn_interpreter(DT_MOVETAB)
def _dyn_interpret_section(content, file, *_):
    try:
        return file.find_at_addr(content)
    except LookupError:
        return content

@_add_dyn_interpreter(DT_INIT_ARRAY)
def _dyn_interpret_init_array(content, file, parent):
    file.memory.seek(content)
    return file.memory.read(parent.find_entry(DT_INIT_ARRAYSZ).content)

##


def _parse_entry_content(d_tag, content, file, parent):
    if d_tag in DYN_INTERPRETERS:
        return DYN_INTERPRETERS[d_tag](content, file, parent)
    return content


###
def _is_pointer(d_tag):
    if d_tag in DYNAMIC_TAG_MAP:
        d_tag_const = DYNAMIC_TAG_MAP[d_tag]
        if d_tag_const in DT_D_VAL:
            return False  # val
        elif d_tag_const in DT_D_PTR:
            return True  # pointer
        else:
            return False
    else:
        return bool(1 - d_tag % 2)


class DynamicEntry:
    def __init__(self, d_tag, d_un, file, parent):
        self.d_tag = DYNAMIC_TAG_MAP.get(d_tag, d_tag)
        self.content = d_un
        self.parent = parent
        self.pointer = _is_pointer(d_tag)
        self.file = file
        self.value = None

    def _interpret_content(self):
        print(self.d_tag)
        self.value = _parse_entry_content(
            self.d_tag, self.content, self.file, self.parent
        )

    def __repr__(self):
        return f"<DynamicEntry {self.d_tag} {self.value}>"


class Dynamic:
    def __init__(self, content, file):
        self.content = content
        self.file = file
        self.buf = BytesIO(self.content)
        self._size = len(self.content)
        self.arch = file.arch
        self.endian = file.endian
        self.entries = []
        while True:
            d_un, d_tag, offset = self._read_one_entry()
            self.entries.append(DynamicEntry(d_tag, d_un, file, self))
            if offset >= self._size:
                break
    def find_entry(self,tag):
        for entry in self.entries:
            if entry.d_tag==tag:
                return entry
    def _read_one_entry(self):
        if self.arch == ARCH_64:
            d_tag = endian_read(self.buf, self.endian, 8)  # 64_Xword
            d_un = endian_read(self.buf, self.endian, 8)  # 64_Addr
        else:
            d_tag = endian_read(self.buf, self.endian, 4)
            d_un = endian_read(self.buf, self.endian, 4)
        return d_un, d_tag, self.buf.tell()

    def _after_init(self):
        for entry in self.entries:
            entry._interpret_content()
