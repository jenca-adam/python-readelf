from ..maps import DT_D_VAL, DT_D_PTR
from ..const import *
from ..helpers import endian_read, split_array
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


def _parse_array(sizetag, itemsize=None):
    def _decorator(func):
        @functools.wraps(func)
        def _inner(content, file, parent):
            file.memory.seek(content)
            data = file.memory.read(parent.find_entry(sizetag).content)
            if itemsize is None:
                array = file._split_array(data)
            else:
                array = split_array(data, itemsize, file.endian)
            return func(array)

        return _inner

    return _decorator


def _strtab_parse():
    def _decorator(func):
        @functools.wraps(func)
        def _inner(content, file, parent):
            arr = func(content, file, parent)
            dynstr = file.find_at_addr(parent.find_entry(DT.DT_STRTAB).content)
            return [dynstr.get_name(i) for i in arr]

        return _inner


##


@_add_dyn_interpreter(DT.DT_SONAME)
@_add_dyn_interpreter(DT.DT_RPATH)
@_add_dyn_interpreter(DT.DT_RUNPATH)
@_add_dyn_interpreter(DT.DT_SUNW_AUXILIARY)
@_add_dyn_interpreter(DT.DT_SUNW_FILTER)
@_add_dyn_interpreter(DT.DT_AUXILIARY)
@_add_dyn_interpreter(DT.DT_FILTER)
@_add_dyn_interpreter(DT.DT_CONFIG)
@_add_dyn_interpreter(DT.DT_DEPAUDIT)
@_add_dyn_interpreter(DT.DT_AUDIT)
@_add_dyn_interpreter(DT.DT_NEEDED)
def _dyn_interpret_in_dynstr(content, file, parent):
    dynstr = file.find_at_addr(parent.find_entry(DT.DT_STRTAB).content)
    return dynstr.get_name(content)


@_add_dyn_interpreter(DT.DT_INIT)
@_add_dyn_interpreter(DT.DT_FINI)
@_add_dyn_interpreter(DT.DT_STRTAB)
@_add_dyn_interpreter(DT.DT_SYMTAB)
@_add_dyn_interpreter(DT.DT_RELA)
@_add_dyn_interpreter(DT.DT_VERNEED)
@_add_dyn_interpreter(DT.DT_SUNW_CAP)
@_add_dyn_interpreter(DT.DT_SYMINFO)
@_add_dyn_interpreter(DT.DT_VERDEF)
@_add_dyn_interpreter(DT.DT_MOVETAB)
def _dyn_interpret_section(content, file, *_):
    try:
        return file.find_at_addr(content)
    except LookupError:
        return content


@_add_dyn_interpreter(DT.DT_INIT_ARRAY)
@_parse_array(DT.DT_INIT_ARRAYSZ)
def _dyn_interpret_init_array(array):
    return array


@_add_dyn_interpreter(DT.DT_FINI_ARRAY)
@_parse_array(DT.DT_FINI_ARRAYSZ)
def _dyn_interpret_fini_array(array):
    return array


@_add_dyn_interpreter(DT.DT_PREINIT_ARRAY)
@_parse_array(DT.DT_PREINIT_ARRAYSZ)
def _dyn_interpret_preinit_array(array):
    return array


##


def _parse_entry_content(d_tag, content, file, parent):
    if d_tag in DYN_INTERPRETERS:
        return DYN_INTERPRETERS[d_tag](content, file, parent)
    return content


###
def _is_pointer(d_tag):
    if d_tag in DT:
        d_tag_const = DT(d_tag)
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
        self.d_tag = DT.get(d_tag, d_tag)
        self.content = d_un
        self.parent = parent
        self.pointer = _is_pointer(d_tag)
        self.file = file
        self.value = None

    def _interpret_content(self):
        self.value = _parse_entry_content(
            self.d_tag, self.content, self.file, self.parent
        )

    def __repr__(self):
        return f"<DynamicEntry {self.d_tag} {self.value}>"


class Dynamic:
    def __init__(self, content, file, *_):
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

    def find_entry(self, tag):
        for entry in self.entries:
            if entry.d_tag == tag:
                return entry

    def _read_one_entry(self):
        if self.arch == ARCH.ARCH_64:
            d_tag = endian_read(self.buf, self.endian, 8)  # 64_Xword
            d_un = endian_read(self.buf, self.endian, 8)  # 64_Addr
        else:
            d_tag = endian_read(self.buf, self.endian, 4)
            d_un = endian_read(self.buf, self.endian, 4)
        return d_un, d_tag, self.buf.tell()

    def _after_init(self):
        for entry in self.entries:
            entry._interpret_content()
