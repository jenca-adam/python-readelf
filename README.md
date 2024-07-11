# python-readelf
`python-readelf` is an ELF file reading library.

## Installation

Not pypi yet. Install from the github repo.

## Documentation

The main entry point is the function `readelf.readelf()`, which takes a file path as an argument.
For example:

```python
>>> file = readelf.readelf("/usr/bin/python3.12")
>>> file.find_section(".text")
<Section .text @ 0x1020>
>>> 
```
### `ELFFile` attributes and methods

#### `find_section_by_type(type)`
Finds a section with a given type.
Type must be a member of the `const.SHT` enum.
If no such section exists, a `LookupError` is raised.
#### `find_sections_by_type(type)`
Finds all sections with a given type, as a `tuple`.
Type must be a member of the `const.SHT` enum.
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

The file's `Memory` object. see [`Memory` attributes and methods](#memory-attributes-and-methods)
#### `sections`

A list of all the sections contained in the file. see [`Section` attributes and methods](#section-attributes-and-methods)

#### `segments`

All the program segments contained in the file.
see [`ProgramSegments` attributes and methods](#programsegments-attributes-and-methods)

#### `__getitem__()`

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

#### `addr`

The memory address where the section starts.

#### `offset`

The file offset where the section starts.

#### `size`

The size of the section's content.

#### `addralign`

Required section alignment.

#### `content`

Raw section content.

#### `parsed_content`

Parsed section content (section type specific)

#### `file`

The ELFFile instance contaning this section.


#### Section type specific attributes/methods

##### `DYNAMIC`

###### `entries`

A list of all the entries in the section.

###### `find_entries(tag)`

Finds an entry with a given tag.

###### `DynamicEntry.d_tag`

The entry tag.

Possible values: 
`const.DT.DT_NULL`, `const.DT.DT_NEEDED`, `const.DT.DT_PLTRELSZ`, `const.DT.DT_PLTGOT`, `const.DT.DT_HASH`, `const.DT.DT_STRTAB`, `const.DT.DT_SYMTAB`, `const.DT.DT_RELA`, `const.DT.DT_RELASZ`, `const.DT.DT_RELAENT`, `const.DT.DT_STRSZ`, `const.DT.DT_SYMENT`, `const.DT.DT_INIT`, `const.DT.DT_FINI`, `const.DT.DT_SONAME`, `const.DT.DT_RPATH`, `const.DT.DT_SYMBOLIC`, `const.DT.DT_REL`, `const.DT.DT_RELSZ`, `const.DT.DT_RELENT`, `const.DT.DT_PLTREL`, `const.DT.DT_DEBUG`, `const.DT.DT_TEXTREL`, `const.DT.DT_JMPREL`, `const.DT.DT_BIND_NOW`, `const.DT.DT_INIT_ARRAY`, `const.DT.DT_FINI_ARRAY`, `const.DT.DT_INIT_ARRAYSZ`, `const.DT.DT_FINI_ARRAYSZ`, `const.DT.DT_RUNPATH`, `const.DT.DT_FLAGS`, `const.DT.DT_ENCODING`, `const.DT.DT_PREINIT_ARRAYSZ`, `const.DT.DT_MAXPOSTAGS`, `const.DT.DT_SUNW_AUXILIARY`, `const.DT.DT_SUNW_FILTER`, `const.DT.DT_SUNW_CAP`, `const.DT.DT_SUNW_SYMTAB`, `const.DT.DT_SUNW_SYMSZ`, `const.DT.DT_SUNW_SORTENT`, `const.DT.DT_SUNW_SYMSORT`, `const.DT.DT_SUNW_SYMSORTSZ`, `const.DT.DT_SUNW_TLSSORT`, `const.DT.DT_SUNW_TLSSORTSZ`, `const.DT.DT_SUNW_CAPINFO`, `const.DT.DT_SUNW_STRPAD`, `const.DT.DT_SUNW_CAPCHAIN`, `const.DT.DT_SUNW_LDMACH`, `const.DT.DT_SUNW_CAPCHAINENT`, `const.DT.DT_SUNW_CAPCHAINSZ`, `const.DT.DT_OS`, `const.DT.DT_VALRNGLO`, `const.DT.DT_CHECKSUM`, `const.DT.DT_PLTPADSZ`, `const.DT.DT_MOVEENT`, `const.DT.DT_MOVESZ`, `const.DT.DT_POSFLAG_1`, `const.DT.DT_SYMINSZ`, `const.DT.DT_SYMINENT`, `const.DT.DT_VALRNGHI`, `const.DT.DT_ADDRRNGLO`, `const.DT.DT_CONFIG`, `const.DT.DT_DEPAUDIT`, `const.DT.DT_AUDIT`, `const.DT.DT_PLTPAD`, `const.DT.DT_MOVETAB`, `const.DT.DT_SYMINFO`, `const.DT.DT_ADDRRNGHI`, `const.DT.DT_RELACOUNT`, `const.DT.DT_RELCOUNT`, `const.DT.DT_FLAGS_1`, `const.DT.DT_VERDEF`, `const.DT.DT_VERDEFNUM`, `const.DT.DT_VERNEED`, `const.DT.DT_VERNEEDNUM`, `const.DT.DT_SPARC_REGISTER`, `const.DT.DT_AUXILIARY`, `const.DT.DT_USED`, `const.DT.DT_FILTER`, `const.DT.DT_PROC`

###### `DynamicEntry.parent`

The parent dynamic section of the entry

###### `DynamicEntry.content`

The raw entry content 

###### `DynamicEntry.value`

The parsed entry content.
This can be a section.


##### `DYNSYM`/`SYMTAB`

######  `symbols`

A list of all the symbols defined in the symbol table

######  `get_symbol(name)`

Finds a symbol with the given name

######  `Sym.name`
The name of the symbol.

###### `Sym.value`

The value of the symbol.


##### `REL`/`RELA`

###### `entries`

A list of all the relocation entries in this section`


###### `Rel(a)Entry.offset`

File offset


###### `Rel(a)Entry.sym`

The relocation symbol

###### `RelaEntry.addend`

A constant relocation addend

### `ProgramSegments` attributes and methods

#### `segments`

A list of all the segments contained within the file.
See [`ProgramSegment` attributes and methods](#programsegment-attributes-and-methods)

### `ProgramSegment` attributes and methods

#### `sections`

A list of all the sections present within the segment

#### `content`

The contents of the segment

#### `readable`

Non-zero if the segment is readable

#### `writable`

Non-zero if the segment is writable

#### `executable`

Non-zero if the segment is executable

#### `type`

Type of the segment.
Possible values: `const.PT.PT_NULL`, `const.PT.PT_LOAD`, `const.PT.PT_DYNAMIC`, `const.PT.PT_INTERP`, `const.PT.PT_NOTE`, `const.PT.PT_SHLIB`, `const.PT.PT_PHDR`, `const.PT.PT_TLS`, `const.PT.PT_OS`, `const.PT.PT_PROC`

#### `vaddr`

Virtual address of the segment in memory.

#### `paddr`

Physical address of the segment in memory.

#### `align`

Segment alignment

### `Memory` attributes and methods

#### `seek(position)`
Moves the memory index to a given position

#### `read(n)`
Reads n bytes from the memory, starting at the current index.

#### `get_section()`
Returns the section allocated to the current index.
Returns `None` if no such section could be found.

#### `__getitem__(index)`
Returns the section allocated to an index.
Returns `None` if no such section could be found.

## Usage

### Opening a file

```python
>>> import readelf
>>> file = readelf.readelf("/usr/bin/python3.12")
#...
```

### Accessing sections

#### By name
```python
>>> file.find_section(".data")
<Section .data @ 0x4000>
```
#### By address
```python
>>> file.find_at_addr(0x4000)
<Section .data @ 0x4000>
```

#### By file offset

```python
>>> file.find_at_offset(12288)
<Section .data @ 0x4000>
```

#### By type

```python
>>> file.find_sections_by_type(elfparser.const.SHT.SHT_PROGBITS)
(<Section .interp @ 0x318>, <Section .init @ 0x1000>, <Section .text @ 0x1020>, <Section .fini @ 0x112c>, <Section .rodata @ 0x2000>, <Section .eh_frame_hdr @ 0x2004>, <Section .eh_frame @ 0x2020>, <Section .got @ 0x3fb8>, <Section .data @ 0x4000>, <Section .comment @ 0x0>, <Section .gnu_debuglink @ 0x0>)
```

### Extracting symbols

```python
>>> python = readelf.readelf("/usr/lib/libpython3.12.so")
>>> dynsym = python.find_section_by_type(elfparser.const.SHT.SHT_DYNSYM) # or find_section(".dynsym")
>>> sym = dynsym.get_symbol("PyExc_ValueError")
>>> sym
<Sym [STT_OBJECT] PyExc_ValueError (22@4da548+8)>
>>> sym.value
b'\x00\x7fM\x00\x00\x00\x00\x00'
```

