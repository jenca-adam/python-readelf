# python-readelf
`python-readelf` is an ELF file reading library.

## Usage

The main entry point is the function `readelf.readelf()`, which takes a file path as an argument.
For example:

```python
>>> file = readelf.readelf("/usr/bin/python3.12")
>>> file.find_section(".text")
<Section .text @ 0x1020>
>>> 
```
### `ELFFile` attributes and methods

#### `find_section(name)`
Returns the first occurence of a section with a given name.
If no such section exists, a `LookupError` is raised.

```python
>>> file = readelf.readelf("/usr/bin/python3.12")
>>> file.find_section(".text")
<Section .text @ 0x1020>
>>> 
```

#### `find_sections(name)`

Returns all the occurences of sections with a given name, as a `tuple`.

#### `find_at_addr(addr)`

Returns the section starting at a given memory address. If no such section exists, a `LookupError` is raised.

```python
>>> file = readelf.readelf("/usr/bin/python3.12")
>>> file.find_at_addr(0x1020)
<Section .text @ 0x1020>
>>>
``` 

#### `find_at_offset(offset)`

Returns the section saved in the file starting at a given file offset. If no such section exists, a `LookupError` is raised.

#### `from_stream(buf)`\[classmethod\]

Creates an ELFFile instance from a stream.

```python
>>> file = ELFFile.from_stream(BytesIO(data)) 
>>>
```

#### `arch`

The architecture the file was compiled for.
Possible values: `const.ARCH.ARCH_64`, `const.ARCH.ARCH_32`

#### `endian`

The file's endianness.
Possible values: `const.ENDIAN.ENDIAN_LITTLE`, `const.ENDIAN.ENDIAN_BIG`

#### `version`

The ELF version the file is using.
Possible values: `const.EI_VER.EI_VER_1`

#### `abi`

The Application Binary Interface the file is using.
Possible values: `const.ABI.ABI_SYSTEMV`, `const.ABI.ABI_HPUX`, `const.ABI.ABI_NETBSD`, `const.ABI.ABI_LINUX`, `const.ABI.ABI_HURD`, `const.ABI.ABI_SOLARIS`, `const.ABI.ABI_AIX`, `const.ABI.ABI_IRIX`, `const.ABI.ABI_FREEBSD`, `const.ABI.ABI_TRU64`, `const.ABI.ABI_MODESTO`, `const.ABI.ABI_OPENBSD`, `const.ABI.ABI_OPENVMS`, `const.ABI.ABI_NONSTOP`, `const.ABI.ABI_AROS`, `const.ABI.ABI_FENIXOS`, `const.ABI.ABI_CLOUDABI`, `const.ABI.ABI_OPENVOS`

#### `type`

The file type, as defined in the ELF specification.
Possible values: `const.ET.ET_NONE`, `const.ET.ET_REL`, `const.ET.ET_EXEC`, `const.ET.ET_DYN`, `const.ET.ET_CORE`, `const.ET.ET_OS`, `const.ET.ET_PROC`

#### `isa`

The Instruction Set Architecture the file was compiled for.

Possible values: `const.ISA.ISA_RESERVED`, `const.ISA.ISA_NONE`, `const.ISA.ISA_ATT`, `const.ISA.ISA_SPARC`, `const.ISA.ISA_X86`, `const.ISA.ISA_M68K`, `const.ISA.ISA_M88K`, `const.ISA.ISA_MCU`, `const.ISA.ISA_I80860`, `const.ISA.ISA_MIPS`, `const.ISA.ISA_IBM370`, `const.ISA.ISA_MIPS3K`, `const.ISA.ISA_PARISC`, `const.ISA.ISA_I80960`, `const.ISA.ISA_POWERPC32`, `const.ISA.ISA_POWERPC64`, `const.ISA.ISA_S390`, `const.ISA.ISA_IBMSPU`, `const.ISA.ISA_NECV800`, `const.ISA.ISA_FR20`, `const.ISA.ISA_TRWRH32`, `const.ISA.ISA_MRCE`, `const.ISA.ISA_ARM`, `const.ISA.ISA_DIGALPH`, `const.ISA.ISA_SUPERH`, `const.ISA.ISA_SPARC9`, `const.ISA.ISA_STRICORE`, `const.ISA.ISA_ARGORISC`, `const.ISA.ISA_H8300`, `const.ISA.ISA_H8300H`, `const.ISA.ISA_H8S`, `const.ISA.ISA_H8500`, `const.ISA.ISA_IA64`, `const.ISA.ISA_MIPSX`, `const.ISA.ISA_COLDFIRE`, `const.ISA.ISA_HC12`, `const.ISA.ISA_FUMMA`, `const.ISA.ISA_SPCP`, `const.ISA.ISA_SRISC`, `const.ISA.ISA_NDR1`, `const.ISA.ISA_STARCORE`, `const.ISA.ISA_ME16`, `const.ISA.ISA_ST100`, `const.ISA.ISA_TINYJ`, `const.ISA.ISA_AMDX8664`, `const.ISA.ISA_SDSP`, `const.ISA.ISA_PDP10`, `const.ISA.ISA_PDP11`, `const.ISA.ISA_FX66`, `const.ISA.ISA_ST9P`, `const.ISA.ISA_ST7`, `const.ISA.ISA_HC16`, `const.ISA.ISA_HC11`, `const.ISA.ISA_HC08`, `const.ISA.ISA_HC05`, `const.ISA.ISA_SVX`, `const.ISA.ISA_ST19`, `const.ISA.ISA_VAX`, `const.ISA.ISA_AXIS`, `const.ISA.ISA_INF`, `const.ISA.ISA_ELEM14`, `const.ISA.ISA_LSI`, `const.ISA.ISA_TMS320C6K`, `const.ISA.ISA_MCS`, `const.ISA.ISA_AARCH`, `const.ISA.ISA_Z80`, `const.ISA.ISA_RISCV`, `const.ISA.ISA_BPF`, `const.ISA.ISA_65C816`

#### `entry`

The file offset where the file starts executing.

```python
>>> elf_file.find_at_offset(elf_file.entry)
<Section .text @ 0x1020>
>>>
```

#### `phoff`

The program header file offset

#### `shoff`

The section header file offset

#### `flags`

The file's flags. Interpretation varies depending on the isa.

#### `ehsize`

The file header size.

#### `phentsize`

The program header entry size.

#### `phnum`

The number of program header entries.

#### `shentsize`

The section header entry size.

#### `shnum`

The number of section header entries.

#### `shstrndx`

The section header string table index.

#### `memory`

The file's `Memory` object. see [`Memory` attributes and methods][#memory-attributes-and-methods]

#### `sections`

A list of all the sections contained in the file. see [`Section` attributes and methods][#section-attributes-and-methods]

#### `segments`

All the program segments contained in the file.
see [`ProgramSegments` attributes and methods][#programsegments-attributes-and-methods]

#### `__getitem__`

You can use `elf_file[n]` to get the nth segment in the file.

### `Section` attributes and methods

#### `name`

The section name from the string table

#### `type`

The section type.
Possible values: `const.SHT.SHT_NULL`, `const.SHT.SHT_PROGBITS`, `const.SHT.SHT_SYMTAB`, `const.SHT.SHT_STRTAB`, `SHT.SHT_RELA`, `SHT.SHT_HASH`, `SHT.SHT_DYNAMIC`, `SHT.SHT_NOTE`, `SHT.SHT_NOBITS`, `SHT.SHT_REL`, `SHT.SHT_SHLIB`, `SHT.SHT_DYNSYM`, `SHT.SHT_INIT_ARRAY`, `SHT.SHT_FINI_ARRAY`, `SHT.SHT_PREINIT_ARRAY`, `SHT.SHT_GROUP`, `SHT.SHT_SYMTAB_SHNDX`, `SHT.SHT_NUM`, `SHT.SHT_OS`

#### `flags`

A set of the section flags.
Possible flags:
`const.SHF.SHF_WRITE`, `const.SHF.SHF_ALLOC`, `const.SHF.SHF_EXECINSTR`, `const.SHF.SHF_MERGE` `const.SHF.SHF_MERGE`, `const.SHF.SHF_STRINGS`, `const.SHF.SHF_INFO_LINK`, `const.SHF.SHF_OS_NONCONFORMING`, `const.SHF.SHF_GROUP`, `const.SHF.SHF_TLS`, `const.SHF.SHF_MASKOS`, `const.SHF.SHF_MASKPROC`, `const.SHF.SHF_ORDERED`, `const.SHF.SHF_EXCLUDE`

