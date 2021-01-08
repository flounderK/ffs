# FFS
FFS is a file format specification language


## Chunks
FFS organizes files into chunks. A chunk can either contain other defined chunks or typed variable. Chunks may be declared out of order, but the layout of the variables and other chunks defined in a chunk must be in order.


## Types
Types can be user-defined or built-in. Built in types include primitive C types, as well as other common aliases for types.

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

## Variables

