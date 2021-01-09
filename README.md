# FFS
FFS is a file format specification language. Its purpose is to allow users to define file formats programatically.


## Chunks
FFS organizes files into chunks. A chunk can either contain other defined chunks or typed fields. Chunks may be declared out of order, but the layout of the variables and other chunks defined in a chunk must be in order.


An example of the ELF header format:
```
ELF_HEADER:

    RAW_BYTE(4)      signature (7F 45 4C 46)  //  0x7F ELF,
                                /* basic type variable declaration */
    BYTE             EI_CLASS ! size_t((01, uint32), (02, uint64))
    BYTE             EI_DATA
    BYTE             EI_VERSION
    BYTE             EI_OSABI
    7B               EI_PAD
    ushort           e_type
    ushort           e_machine
    $size_t          e_entry
    $size_t          e_phoff
    $size_t          e_shoff
    ushort           e_ehsize
    ushort           e_phentsize
    ushort           e_phnum
    ushort           e_shentsize
    ushort           e_shnum
    ushort           e_shstrndx

```


## Types
Types can be user-defined or built-in. Built in types include primitive C types, as well as other common aliases for types. For unusually sized types that will be used only once, struct packing codes can be used in place of a type name to define the size. Types can also be defined by type variables.

## Type Aliases
Aliases can be used to refer to an existing type with a user-defined name. Aliases are useful for matching up types defined in code for a file format parser up to a file format specification.
```
typealias MyHeader uint32
```

## Defining Types
Types can be defined by using C struct packing codes:
```
typedef ten_bytes 10B
```

## Type Variables
While fields of a chunk can be used as variables (often to determine the number of elements in an array), fields can also be used to set variables that determine which types are used for other fields.


