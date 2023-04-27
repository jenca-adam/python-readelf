import importlib

_CONST = importlib.import_module(__name__)


class _Spec:
    def __repr__(self):
        return self.__class__.__qualname__


_SPEC_NAMES = [
    # archs
    "ARCH_32",
    "ARCH_64",
    # endians
    "ENDIAN_BIG",
    "ENDIAN_LITTLE",
    # versions
    "EI_VER_1",
    # abis
    "ABI_SYSTEMV",
    "ABI_HPUX",
    "ABI_NETBSD",
    "ABI_LINUX",
    "ABI_HURD",
    "ABI_SOLARIS",
    "ABI_AIX",
    "ABI_IRIX",
    "ABI_FREEBSD",
    "ABI_TRU64",
    "ABI_MODESTO",
    "ABI_OPENBSD",
    "ABI_OPENVMS",
    "ABI_NONSTOP",
    "ABI_AROS",
    "ABI_FENIXOS",
    "ABI_CLOUDABI",
    "ABI_OPENVOS",
    # ets
    "ET_NONE",
    "ET_REL",
    "ET_EXEC",
    "ET_DYN",
    "ET_CORE",
    "ET_OS",
    "ET_PROC",
    # isas (i wanna die)
    "ISA_RESERVED",
    "ISA_NONE",
    "ISA_ATT",
    "ISA_SPARC",
    "ISA_X86",
    "ISA_M68K",
    "ISA_M88K",
    "ISA_MCU",
    "ISA_I80860",
    "ISA_MIPS",
    "ISA_IBM370",
    "ISA_MIPS3K",
    "ISA_PARISC",
    "ISA_I80960",
    "ISA_POWERPC32",
    "ISA_POWERPC64",
    "ISA_S390",
    "ISA_IBMSPU",
    "ISA_NECV800",
    "ISA_FR20",  # bruh like fr?
    "ISA_TRWRH32",
    "ISA_MRCE",
    "ISA_ARM",
    "ISA_DIGALPH",
    "ISA_SUPERH",
    "ISA_SPARC9",
    "ISA_STRICORE",
    "ISA_ARGORISC",
    "ISA_H8300",
    "ISA_H8300H",
    "ISA_H8S",
    "ISA_H8500",
    "ISA_IA64",
    "ISA_MIPSX",
    "ISA_COLDFIRE",
    "ISA_HC12",
    "ISA_FUMMA",
    "ISA_SPCP",
    "ISA_SRISC",
    "ISA_NDR1",
    "ISA_STARCORE",
    "ISA_ME16",
    "ISA_ST100",
    "ISA_TINYJ",
    "ISA_AMDX8664",
    "ISA_SDSP",
    "ISA_PDP10",
    "ISA_PDP11",
    "ISA_FX66",
    "ISA_ST9P",
    "ISA_ST7",
    "ISA_HC16",
    "ISA_HC11",
    "ISA_HC08",
    "ISA_HC05",
    "ISA_SVX",
    "ISA_ST19",
    "ISA_VAX",
    "ISA_AXIS",
    "ISA_INF",
    "ISA_ELEM14",
    "ISA_LSI",
    "ISA_TMS320C6K",
    "ISA_MCST",
    "ISA_AARCH",  # or ArmV8
    "ISA_Z80",
    "ISA_RISCV",
    "ISA_BPF",
    "ISA_65C816",
]
for _i in _SPEC_NAMES:

    class _REPL(_Spec):
        __qualname__ = _i
        __name__ = _i

    setattr(_CONST, _i, _REPL())
