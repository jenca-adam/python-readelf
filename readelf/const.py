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

    @classmethod
    def from_dw_endian(cls, dw_endian):
        return cls(3 - dw_endian.value)  # switcharoo


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
    ISA_I80860 = 0x08
    ISA_MIPS = 0x09
    ISA_IBM370 = 0x0A
    ISA_MIPS3K = 0x0B
    ISA_PARISC = 0x0E
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


## dwarves


class DW_UT(enum.Enum, metaclass=ContainsEnum):
    DW_UT_compile = 0x01
    DW_UT_type = 0x02
    DW_UT_partial = 0x03
    DW_UT_skeleton = 0x04
    DW_UT_split_compile = 0x05
    DW_UT_split_type = 0x06


class DW_TAG(enum.Enum, metaclass=ContainsEnum):

    DW_TAG_array_type = 0x01
    DW_TAG_class_type = 0x02
    DW_TAG_entry_point = 0x03
    DW_TAG_enumeration_type = 0x04
    DW_TAG_formal_parameter = 0x05

    DW_TAG_imported_declaration = 0x08

    DW_TAG_label = 0x0A
    DW_TAG_lexical_block = 0x0B

    DW_TAG_member = 0x0D

    DW_TAG_pointer_type = 0x0F
    DW_TAG_reference_type = 0x10
    DW_TAG_compile_unit = 0x11
    DW_TAG_string_type = 0x12
    DW_TAG_structure_type = 0x13

    DW_TAG_subroutine_type = 0x15
    DW_TAG_typedef = 0x16
    DW_TAG_union_type = 0x17
    DW_TAG_unspecified_parameters = 0x18
    DW_TAG_variant = 0x19
    DW_TAG_common_block = 0x1A
    DW_TAG_common_inclusion = 0x1B
    DW_TAG_inheritance = 0x1C
    DW_TAG_inlined_subroutine = 0x1D
    DW_TAG_module = 0x1E

    DW_TAG_ptr_to_member_type = 0x1F
    DW_TAG_set_type = 0x20
    DW_TAG_subrange_type = 0x21
    DW_TAG_with_stmt = 0x22
    DW_TAG_access_declaration = 0x23
    DW_TAG_base_type = 0x24
    DW_TAG_catch_block = 0x25
    DW_TAG_const_type = 0x26
    DW_TAG_constant = 0x27
    DW_TAG_enumerator = 0x28
    DW_TAG_file_type = 0x29
    DW_TAG_friend = 0x2A
    DW_TAG_namelist = 0x2B
    DW_TAG_namelist_item = 0x2C
    DW_TAG_packed_type = 0x2D
    DW_TAG_subprogram = 0x2E
    DW_TAG_template_type_parameter = 0x2F
    DW_TAG_template_value_parameter = 0x30
    DW_TAG_thrown_type = 0x31
    DW_TAG_try_block = 0x32
    DW_TAG_variant_part = 0x33
    DW_TAG_variable = 0x34
    DW_TAG_volatile_type = 0x35
    DW_TAG_dwarf_procedure = 0x36
    DW_TAG_restrict_type = 0x37
    DW_TAG_interface_type = 0x38
    DW_TAG_namespace = 0x39
    DW_TAG_imported_module = 0x3A
    DW_TAG_unspecified_type = 0x3B
    DW_TAG_partial_unit = 0x3C
    DW_TAG_imported_unit = 0x3D

    DW_TAG_condition = 0x3F
    DW_TAG_shared_type = 0x40
    DW_TAG_type_unit = 0x41
    DW_TAG_rvalue_reference_type = 0x42
    DW_TAG_template_alias = 0x43
    DW_TAG_coarray_type = 0x44
    DW_TAG_generic_subrange = 0x45
    DW_TAG_dynamic_type = 0x46
    DW_TAG_atomic_type = 0x47
    DW_TAG_call_site = 0x48
    DW_TAG_call_site_parameter = 0x49
    DW_TAG_skeleton_unit = 0x4A
    DW_TAG_immutable_type = 0x4B


class DW_AT(enum.Enum, metaclass=ContainsEnum):
    DW_AT_sibling = 0x01
    DW_AT_location = 0x02
    DW_AT_name = 0x03

    DW_AT_ordering = 0x09

    DW_AT_byte_size = 0x0B

    DW_AT_bit_size = 0x0D

    DW_AT_stmt_list = 0x10
    DW_AT_low_pc = 0x11
    DW_AT_high_pc = 0x12
    DW_AT_language = 0x13

    DW_AT_discr = 0x15
    DW_AT_discr_value = 0x16
    DW_AT_visibility = 0x17
    DW_AT_import = 0x18
    DW_AT_string_length = 0x19
    DW_AT_common_reference = 0x1A
    DW_AT_comp_dir = 0x1B
    DW_AT_const_value = 0x1C
    DW_AT_containing_type = 0x1D
    DW_AT_default_value = 0x1E

    DW_AT_inline = 0x20
    DW_AT_is_optional = 0x21
    DW_AT_lower_bound = 0x22

    DW_AT_producer = 0x25

    DW_AT_prototyped = 0x27

    DW_AT_return_addr = 0x2A

    DW_AT_start_scope = 0x2C

    DW_AT_bit_stride = 0x2E
    DW_AT_upper_bound = 0x2F

    DW_AT_abstract_origin = 0x31
    DW_AT_accessibility = 0x32
    DW_AT_address_class = 0x33
    DW_AT_artiﬁcial = 0x34
    DW_AT_base_types = 0x35
    DW_AT_calling_convention = 0x36
    DW_AT_count = 0x37
    DW_AT_data_member_location = 0x38
    DW_AT_decl_column = 0x39
    DW_AT_decl_ﬁle = 0x3A
    DW_AT_decl_line = 0x3B
    DW_AT_declaration = 0x3C
    DW_AT_discr_list = 0x3D
    DW_AT_encoding = 0x3E
    DW_AT_external = 0x3F
    DW_AT_frame_base = 0x40
    DW_AT_friend = 0x41
    DW_AT_identiﬁer_case = 0x42

    DW_AT_namelist_item = 0x44
    DW_AT_priority = 0x45
    DW_AT_segment = 0x46
    DW_AT_speciﬁcation = 0x47
    DW_AT_static_link = 0x48
    DW_AT_type = 0x49
    DW_AT_use_location = 0x4A
    DW_AT_variable_parameter = 0x4B
    DW_AT_virtuality = 0x4C
    DW_AT_vtable_elem_location = 0x4D
    DW_AT_allocated = 0x4E
    DW_AT_associated = 0x4F
    DW_AT_data_location = 0x50
    DW_AT_byte_stride = 0x51
    DW_AT_entry_pc = 0x52
    DW_AT_use_UTF8 = 0x53
    DW_AT_extension = 0x54
    DW_AT_ranges = 0x55
    DW_AT_trampoline = 0x56
    DW_AT_call_column = 0x57
    DW_AT_call_ﬁle = 0x58
    DW_AT_call_line = 0x59
    DW_AT_description = 0x5A
    DW_AT_binary_scale = 0x5B
    DW_AT_decimal_scale = 0x5C
    DW_AT_small = 0x5D
    DW_AT_decimal_sign = 0x5E
    DW_AT_digit_count = 0x5F
    DW_AT_picture_string = 0x60

    DW_AT_mutable = 0x61
    DW_AT_threads_scaled = 0x62
    DW_AT_explicit = 0x63
    DW_AT_object_pointer = 0x64
    DW_AT_endianity = 0x65
    DW_AT_elemental = 0x66
    DW_AT_pure = 0x67
    DW_AT_recursive = 0x68
    DW_AT_signature = 0x69
    DW_AT_main_subprogram = 0x6A
    DW_AT_data_bit_offset = 0x6B
    DW_AT_const_expr = 0x6C
    DW_AT_enum_class = 0x6D
    DW_AT_linkage_name = 0x6E
    DW_AT_string_length_bit_size = 0x6F
    DW_AT_string_length_byte_size = 0x70
    DW_AT_rank = 0x71
    DW_AT_str_offsets_base = 0x72
    DW_AT_addr_base = 0x73
    DW_AT_rnglists_base = 0x74

    DW_AT_dwo_name = 0x76
    DW_AT_reference = 0x77
    DW_AT_rvalue_reference = 0x78
    DW_AT_macros = 0x79
    DW_AT_call_all_calls = 0x7A
    DW_AT_call_all_source_calls = 0x7B
    DW_AT_call_all_tail_calls = 0x7C
    DW_AT_call_return_pc = 0x7D
    DW_AT_call_value = 0x7E
    DW_AT_call_origin = 0x7F
    DW_AT_call_parameter = 0x80

    DW_AT_call_pc = 0x81
    DW_AT_call_tail_call = 0x82
    DW_AT_call_target = 0x83
    DW_AT_call_target_clobbered = 0x84
    DW_AT_call_data_location = 0x85
    DW_AT_call_data_value = 0x86
    DW_AT_noreturn = 0x87
    DW_AT_alignment = 0x88
    DW_AT_export_symbols = 0x89
    DW_AT_deleted = 0x8A
    DW_AT_defaulted = 0x8B
    DW_AT_loclists_base = 0x8C

    DW_AT_null = 0x00


class DW_FORM(enum.Enum, metaclass=ContainsEnum):
    DW_FORM_addr = 0x01
    DW_FORM_block2 = 0x03
    DW_FORM_block4 = 0x04
    DW_FORM_data2 = 0x05
    DW_FORM_data4 = 0x06
    DW_FORM_data8 = 0x07
    DW_FORM_string = 0x08
    DW_FORM_block = 0x09
    DW_FORM_block1 = 0x0A
    DW_FORM_data1 = 0x0B
    DW_FORM_flag = 0x0C
    DW_FORM_sdata = 0x0D
    DW_FORM_strp = 0x0E
    DW_FORM_udata = 0x0F
    DW_FORM_ref_addr = 0x10
    DW_FORM_ref1 = 0x11
    DW_FORM_ref2 = 0x12
    DW_FORM_ref4 = 0x13
    DW_FORM_ref8 = 0x14
    DW_FORM_ref_udata = 0x15
    DW_FORM_indirect = 0x16
    DW_FORM_sec_offset = 0x17
    DW_FORM_exprloc = 0x18
    DW_FORM_flag_present = 0x19
    DW_FORM_strx = 0x1A
    DW_FORM_addrx = 0x1B
    DW_FORM_ref_sup4 = 0x1C
    DW_FORM_strp_sup = 0x1D
    DW_FORM_data16 = 0x1E
    DW_FORM_line_strp = 0x1F
    DW_FORM_ref_sig8 = 0x20
    DW_FORM_implicit_const = 0x21
    DW_FORM_loclistx = 0x22
    DW_FORM_rnglistx = 0x23
    DW_FORM_ref_sup8 = 0x24
    DW_FORM_strx1 = 0x25
    DW_FORM_strx2 = 0x26
    DW_FORM_strx3 = 0x27
    DW_FORM_strx4 = 0x28
    DW_FORM_addrx1 = 0x29
    DW_FORM_addrx2 = 0x2A
    DW_FORM_addrx3 = 0x2B
    DW_FORM_addrx4 = 0x2C
    DW_FORM_null = 0x00


class DW_LANG(enum.Enum, metaclass=ContainsEnum):
    DW_LANG_C89 = 0x0001
    DW_LANG_C = 0x0002
    DW_LANG_Ada83 = 0x0003
    DW_LANG_C_plus_plus = 0x0004
    DW_LANG_Cobol74 = 0x0005
    DW_LANG_Cobol85 = 0x0006
    DW_LANG_Fortran77 = 0x0007
    DW_LANG_Fortran90 = 0x0008
    DW_LANG_Pascal83 = 0x0009
    DW_LANG_Modula2 = 0x000A
    DW_LANG_Java = 0x000B
    DW_LANG_C99 = 0x000C
    DW_LANG_Ada95 = 0x000D
    DW_LANG_Fortran95 = 0x000E
    DW_LANG_PLI = 0x000F
    DW_LANG_ObjC = 0x0010
    DW_LANG_ObjC_plus_plus = 0x0011
    DW_LANG_UPC = 0x0012
    DW_LANG_D = 0x0013
    DW_LANG_Python = 0x0014
    DW_LANG_OpenCL = 0x0015
    DW_LANG_Go = 0x0016
    DW_LANG_Modula3 = 0x0017
    DW_LANG_Haskell = 0x0018
    DW_LANG_C_plus_plus_03 = 0x0019
    DW_LANG_C_plus_plus_11 = 0x001A
    DW_LANG_OCaml = 0x001B
    DW_LANG_Rust = 0x001C
    DW_LANG_C11 = 0x001D
    DW_LANG_Swift = 0x001E
    DW_LANG_Julia = 0x001F
    DW_LANG_Dylan = 0x0020
    DW_LANG_C_plus_plus_14 = 0x0021
    DW_LANG_Fortran03 = 0x0022
    DW_LANG_Fortran08 = 0x0023
    DW_LANG_RenderScript = 0x0024
    DW_LANG_BLISS = 0x0025
    DW_LANG_lo_user = 0x8000
    DW_LANG_hi_user = 0xFFFF


class DW_ATE(enum.Enum, metaclass=ContainsEnum):
    DW_ATE_address = 0x01
    DW_ATE_boolean = 0x02
    DW_ATE_complex_float = 0x03
    DW_ATE_float = 0x04
    DW_ATE_signed = 0x05
    DW_ATE_signed_char = 0x06
    DW_ATE_unsigned = 0x07
    DW_ATE_unsigned_char = 0x08
    DW_ATE_imaginary_float = 0x09
    DW_ATE_packed_decimal = 0x10
    DW_ATE_numeric_string = 0x11
    DW_ATE_edited = 0x12
    DW_ATE_signed_fixed = 0x0D
    DW_ATE_unsigned_fixed = 0x0E
    DW_ATE_decimal_float = 0x0F
    DW_ATE_UTF = 0x10
    DW_ATE_UCS = 0x11
    DW_ATE_ASCII = 0x12
    DW_ATE_lo_user = 0x80
    DW_ATE_hi_user = 0xFF


class DW_END(enum.Enum, metaclass=ContainsEnum):
    DW_END_default = 0x00
    DW_END_big = 0x01
    DW_END_little = 0x02
    DW_END_lo_user = 0x40
    DW_END_hi_user = 0xFF

    @classmethod
    def from_endian(cls, endian):
        if endian == ENDIAN.ENDIAN_LITTLE:
            return cls.DW_END_little
        elif endian == ENDIAN.ENDIAN_BIG:
            return cls.DW_END_big
        raise LookupError


class DW_LNCT(enum.Enum, metaclass=ContainsEnum):
    DW_LNCT_path = 0x01
    DW_LNCT_directory_index = 0x02
    DW_LNCT_timestamp = 0x03
    DW_LNCT_size = 0x04
    DW_LNCT_MD5 = 0x05
    DW_LNCT_lo_user = 0x2000
    DW_LNCT_hi_user = 0x3FFF
