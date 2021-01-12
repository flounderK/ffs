# FFS
FFS is a file format specification language. Its purpose is to allow users to define file formats programmatically.


## Chunks
FFS organizes files into chunks. A chunk can either contain other defined chunks or typed fields. Chunks may be declared out of order, but the layout of the variables and other chunks defined in a chunk must be in order.


An example of the ELF header format:
```
ELF_HEADER:
    // set endianness to big
    ! ENDIAN(BE)

    RAW_BYTE(4)      signature (7F 45 4C 46)  //  0x7F ELF,
                                /* basic type variable declaration */
    BYTE             EI_CLASS ! VAR(size_t, (01, uint32), (02, uint64))
    BYTE             EI_DATA
    BYTE             EI_VERSION
    BYTE             EI_OSABI
    7B               EI_PAD     // inline typedef example
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
Types can be user-defined or built-in. Built in types include primitive C types, as well as other common aliases for types. For unusually sized types that will be used only once, python struct packing codes can be used in place of a type name to define the size. Types can also be defined by type variables.

## Type Aliases
Aliases can be used to refer to an existing type with a user-defined name. Aliases are useful for matching up types defined in code for a file format parser up to a file format specification.
```
typealias MyHeader uint32
```

## Defining Types
Types can be defined by using python struct packing codes, however this invalidates the new type name as a potential candidate for field names:
```
typedef ten_bytes 10B
```

## Type Variables
While fields of a chunk can be used as variables (often to determine the number of elements in an array), fields can also be used to set variables that determine which types are used for other fields.


## Attribute Modifiers
The attributes of chunks and fields can be modified with attribute modifiers.
The following would set a specific field to little endian:
```
main_chunk:
    ! ENDIAN(BE)

    uint32      le_field ! ENDIAN(LE)  // this field is little endian now
    uint32      be_field               /* this field is big endian still,
                                          because it inherits the endianness from the
                                          chunk that owns it*/
```

## Chunk Arrays
It is common for the field of a chunk to contain a variable number of another type of chunk within it. As long as the number of elements in the array is defined somewhere within the spec, ffs can handle it with the following syntax:
```
main_chunk:
    int8                        num_entries
    $other_chunk[$num_entries]  other_chunks

other_chunk:
    int16     some_field
    uint32    some_other_field

```

## Chunk and Field alignment
Certain file types require chunks or fields to be aligned by specific values, either to other chunks, other fields, or the base of the file. This can be achieved with the `ALIGN`, `ALIGN_CHUNK`, `ALIGN_FIELD`, and `ALIGN_FILE` attribute modifiers.

```
main_chunk:
    uint8         version
    $data_chunk   data ! ALIGN_CHUNK(4, $main_chunk)  /* this field (or more specifically
                                                   the chunk that will be expanded here)
                                                   will now be aligned to a multiple of 4 from
                                                   the start of the main chunk*/

data_chunk:
    int     some_field
```

## Bitfields and Enums
Bitfields can be declared by adding the `BITFIELD` modifier to a chunk, however all bitfields must be declared as a multiple of 8, as alternative byte sizes are not supported. Additionally, enums may optionally be defined to support bitfields either inline or globally. Enums do not need to handle every single possibility for a field.
```
main_chunk:
    $bitfield1_chunk         bitfield1

bitfield1_type_enum:
    ! ENUM(32)   // specifies that this chunk defines an enum with 32 different possibilities
    TYPE_A(4)    // TYPE_A will hold the value 4
    TYPE_B(7)
    TYPE_C(6)


bitfield1_chunk:
    ! BITFIELD(8)  // designate this chunk as a bitfield with 8 bits

    BITS(5)               type ! ENUM($bitfield1_type_enum) // types will be referencing the enum 'bitfield1_type_enum'
    BIT                   is_child
    BITS(2)               something  ! ENUM((SOMETHING_1, 01), (SOMETHING_2, 02))  // inline enum declaration


```




