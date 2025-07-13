import enum


class ContainsEnum(enum.EnumMeta):
    def __contains__(cls, value):
        return any(value == item.value for item in cls)

    def get(cls, value, default=None):
        if value in cls:
            return cls(value)
        return default


class ARCH(enum.Enum, metaclass=ContainsEnum):
    # archs
    ARCH_32 = 0x1
    ARCH_64 = 0x2


class ENDIAN(enum.Enum, metaclass=ContainsEnum):
    # endians
    ENDIAN_BIG = 0x2
    ENDIAN_LITTLE = 0x1


class EI_VER(enum.Enum, metaclass=ContainsEnum):
    # versions
    EI_VER_1 = 0x1


class ABI(enum.Enum, metaclass=ContainsEnum):
    # Application Binary interfaces
    ABI_SYSTEMV = 0x0
    ABI_HPUX = 0x01
    ABI_NETBSD = 0x02
    ABI_LINUX = 0x03
    ABI_HURD = 0x04
    ABI_SOLARIS = 0x06
    ABI_AIX = 0x07
    ABI_IRIX = 0x08
    ABI_FREEBSD = 0x09
    ABI_TRU64 = 0x0A
    ABI_MODESTO = 0x0B
    ABI_OPENBSD = 0x0C
    ABI_OPENVMS = 0x0D
    ABI_NONSTOP = 0x0E
    ABI_AROS = 0x0F
    ABI_FENIXOS = 0x10
    ABI_CLOUDABI = 0x11
    ABI_OPENVOS = 0x12


class ET(enum.Enum, metaclass=ContainsEnum):
    # Object file types
    ET_NONE = 0x0
    ET_REL = 0x1
    ET_EXEC = 0x2
    ET_DYN = 0x3
    ET_CORE = 0x4
    ET_OS = 0xFFFE
    ET_PROC = 0xFFFF


class ISA(enum.Enum, metaclass=ContainsEnum):
    # Instruction Architecture sets
    ISA_RESERVED = 0xFFFF
    ISA_NONE = 0x00
    ISA_ATT = 0x01
    ISA_SPARC = 0x02
    ISA_X86 = 0x03
    ISA_M68K = 0x04
    ISA_M88K = 0x05
    ISA_MCU = 0x06
    ISA_I80860 = 0x07
    ISA_MIPS = 0x08
    ISA_IBM370 = 0x09
    ISA_MIPS3K = 0x0A
    ISA_PARISC = 0x0F
    ISA_I80960 = 0x13
    ISA_POWERPC32 = 0x14
    ISA_POWERPC64 = 0x15
    ISA_S390 = 0x16
    ISA_IBMSPU = 0x17
    ISA_NECV800 = 0x18
    ISA_FR20 = 0x24
    ISA_TRWRH32 = 0x25
    ISA_MRCE = 0x27
    ISA_ARM = 0x28
    ISA_DIGALPH = 0x29
    ISA_SUPERH = 0x2A
    ISA_SPARC9 = 0x2B
    ISA_STRICORE = 0x2C
    ISA_ARGORISC = 0x2D
    ISA_H8300 = 0x2E
    ISA_H8300H = 0x2F
    ISA_H8S = 0x30
    ISA_H8500 = 0x31
    ISA_IA64 = 0x32
    ISA_MIPSX = 0x33
    ISA_COLDFIRE = 0x34
    ISA_HC12 = 0x35
    ISA_FUMMA = 0x36
    ISA_SPCP = 0x37
    ISA_SRISC = 0x38
    ISA_NDR1 = 0x39
    ISA_STARCORE = 0x3A
    ISA_ME16 = 0x3B
    ISA_ST100 = 0x3C
    ISA_TINYJ = 0x3D
    ISA_AMDX8664 = 0x3E
    ISA_SDSP = 0x3F
    ISA_PDP10 = 0x40
    ISA_PDP11 = 0x41
    ISA_FX66 = 0x42
    ISA_ST9P = 0x43
    ISA_ST7 = 0x44
    ISA_HC16 = 0x45
    ISA_HC11 = 0x46
    ISA_HC08 = 0x47
    ISA_HC05 = 0x48
    ISA_SVX = 0x49
    ISA_ST19 = 0x4A
    ISA_VAX = 0x4B
    ISA_AXIS = 0x4C
    ISA_INF = 0x4D
    ISA_ELEM14 = 0x4E
    ISA_LSI = 0x4F
    ISA_TMS320C6K = 0x8C
    ISA_MCS = 0xAF
    ISA_AARCH = 0xB7  # or ArmV8
    ISA_Z80 = 0xDC
    ISA_RISCV = 0xF3
    ISA_BPF = 0xF7
    ISA_65C816 = 0x101


class PT(enum.Enum, metaclass=ContainsEnum):
    # Program Header Segment Types
    PT_NULL = 0x0
    PT_LOAD = 0x1
    PT_DYNAMIC = 0x2
    PT_INTERP = 0x3
    PT_NOTE = 0x4
    PT_SHLIB = 0x5
    PT_PHDR = 0x6
    PT_TLS = 0x7
    PT_OS = 0xFE
    PT_PROC = 0xFF


class SHT(enum.Enum, metaclass=ContainsEnum):
    # Section header types
    SHT_NULL = 0x0
    SHT_PROGBITS = 0x1
    SHT_SYMTAB = 0x2
    SHT_STRTAB = 0x3
    SHT_RELA = 0x4
    SHT_HASH = 0x5
    SHT_DYNAMIC = 0x6
    SHT_NOTE = 0x7
    SHT_NOBITS = 0x8
    SHT_REL = 0x9
    SHT_SHLIB = 0x0A
    SHT_DYNSYM = 0x0B
    SHT_INIT_ARRAY = 0x0E
    SHT_FINI_ARRAY = 0x0F
    SHT_PREINIT_ARRAY = 0x10
    SHT_GROUP = 0x11
    SHT_SYMTAB_SHNDX = 0x12
    SHT_NUM = 0x13
    SHT_OS = 0xFF


class SHF(enum.Enum, metaclass=ContainsEnum):
    # Section header flags
    SHF_WRITE = 0x1
    SHF_ALLOC = 0x2
    SHF_EXECINSTR = 0x4
    SHF_MERGE = 0x10
    SHF_STRINGS = 0x20
    SHF_INFO_LINK = 0x40
    SHF_LINK_ORDER = 0x80
    SHF_OS_NONCONFORMING = 0x100
    SHF_GROUP = 0x200
    SHF_TLS = 0x400
    SHF_MASKOS = 0x0FF00000
    SHF_MASKPROC = 0xF0000000
    SHF_ORDERED = 0x4000000
    SHF_EXCLUDE = 0x8000000


class SHN(enum.Enum, metaclass=ContainsEnum):
    # Special section indexes
    SHN_UNDEF = 0x0
    SHN_RESERVE = 0xFF00
    SHN_OS = 0xFF01
    SHN_PROC = 0xFF02
    SHN_ABS = 0xFFF1
    SHN_COMMON = 0xFFF2
    SHN_XINDEX = 0xFFFF
    SHN_INDEX = 0xFFF0


class DT(enum.Enum, metaclass=ContainsEnum):
    # Dynamic entry types
    DT_NULL = 0x0
    DT_NEEDED = 0x1
    DT_PLTRELSZ = 0x2
    DT_PLTGOT = 0x3
    DT_HASH = 0x4
    DT_STRTAB = 0x5
    DT_SYMTAB = 0x6
    DT_RELA = 0x7
    DT_RELASZ = 0x8
    DT_RELAENT = 0x9
    DT_STRSZ = 0x0A
    DT_SYMENT = 0x0B
    DT_INIT = 0x0C
    DT_FINI = 0x0D
    DT_SONAME = 0x0E
    DT_RPATH = 0x0F
    DT_SYMBOLIC = 0x10
    DT_REL = 0x11
    DT_RELSZ = 0x12
    DT_RELENT = 0x13
    DT_PLTREL = 0x14
    DT_DEBUG = 0x15
    DT_TEXTREL = 0x16
    DT_JMPREL = 0x17
    DT_BIND_NOW = 0x18
    DT_INIT_ARRAY = 0x19
    DT_FINI_ARRAY = 0x1A
    DT_INIT_ARRAYSZ = 0x1B
    DT_FINI_ARRAYSZ = 0x1C
    DT_RUNPATH = 0x1D
    DT_FLAGS = 0x1E
    DT_ENCODING = 0x20
    DT_PREINIT_ARRAY = 0x20
    DT_PREINIT_ARRAYSZ = 0x21
    DT_MAXPOSTAGS = 0x22
    DT_SUNW_AUXILIARY = 0x6000000D
    DT_SUNW_FILTER = 0x6000000E

    DT_SUNW_RTLDINF = 0x6000000E
    DT_SUNW_CAP = 0x600000010
    DT_SUNW_SYMTAB = 0x60000011
    DT_SUNW_SYMSZ = 0x60000012
    DT_SUNW_SORTENT = 0x60000013
    DT_SUNW_SYMSORT = 0x60000014
    DT_SUNW_SYMSORTSZ = 0x60000015
    DT_SUNW_TLSSORT = 0x60000016
    DT_SUNW_TLSSORTSZ = 0x60000017
    DT_SUNW_CAPINFO = 0x60000018
    DT_SUNW_STRPAD = 0x600000019
    DT_SUNW_CAPCHAIN = 0x6000001A
    DT_SUNW_LDMACH = 0x6000001B
    DT_SUNW_CAPCHAINENT = 0x6000001D
    DT_SUNW_CAPCHAINSZ = 0x6000001F
    DT_OS = 0xFFFFFFFA
    DT_VALRNGLO = 0x6FFFFD00
    DT_CHECKSUM = 0x6FFFFDF8
    DT_PLTPADSZ = 0x6FFFFDF9
    DT_MOVEENT = 0x6FFFFDFA
    DT_MOVESZ = 0x6FFFFDFB
    DT_POSFLAG_1 = 0x6FFFFDFD
    DT_SYMINSZ = 0x6FFFFDFE
    DT_SYMINENT = 0x6FFFFDFF
    DT_VALRNGHI = 0xFFFFFFFB
    DT_ADDRRNGLO = 0x6FFFFE00
    DT_CONFIG = 0x6FFFFEFA
    DT_DEPAUDIT = 0x6FFFFEFB
    DT_AUDIT = 0x6FFFFEFC
    DT_PLTPAD = 0x6FFFFEFD
    DT_MOVETAB = 0x6FFFFEFE
    DT_SYMINFO = 0x6FFFFEFF
    DT_ADDRRNGHI = 0xFFFFFFFC
    DT_RELACOUNT = 0x6FFFFFF9
    DT_RELCOUNT = 0x6FFFFFFA
    DT_FLAGS_1 = 0x6FFFFFFB
    DT_VERDEF = 0x6FFFFFFC
    DT_VERDEFNUM = 0x6FFFFFFD
    DT_VERNEED = 0x6FFFFFFE
    DT_VERNEEDNUM = 0x6FFFFFFF
    DT_SPARC_REGISTER = 0x70000001
    DT_AUXILIARY = 0x7FFFFFFD
    DT_USED = 0x7FFFFFFE
    DT_FILTER = 0x7FFFFFFF
    DT_PROC = 0xFFFFFFFD


class STB(enum.Enum, metaclass=ContainsEnum):
    STB_LOCAL = 0
    STB_GLOBAL = 1
    STB_WEAK = 2
    STB_OS = 10
    STB_PROC = 13


class STT(enum.Enum, metaclass=ContainsEnum):
    STT_NOTYPE = 0
    STT_OBJECT = 1
    STT_FUNC = 2
    STT_SECTION = 3
    STT_FILE = 4
    STT_COMMON = 5
    STT_TLS = 6
    STT_OS = 11
    STT_SPARC_REGISTER = 13
    STT_PROC = 14


class STV(enum.Enum, metaclass=ContainsEnum):
    STV_DEFAULT = 0
    STV_INTERNAL = 1
    STV_HIDDEN = 2
    STV_PROTECTED = 3
    STV_EXPORTED = 4
    STV_SINGLETON = 5
    STV_ELIMINATE = 6
