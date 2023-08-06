
# cla.f90 is a module for parsing command-line arguments in Fortran-90.

## Features

-    Handles key/value pairs and flags in arbitrary order on the command line.

-    Includes validation and error messages for invalid or ill-formed command line arguments.

-    Is aware of help flags (--help, etc) by default.

-    Values passed as arguments can be character string, integer, real, or boolean.

-    Depends on kinds.f90 for specification of size of strings, integers, reals, and pointers.

-    Uses the F03 standard for accessing the command line arguments (`command_argument_count` and `get_command_argument`).

-    Tested with gfortran, ifort, and pgf90.

-    See cla_test.f90 for an example of usage.

## Usage Example

     use cla
     ...
     call cla_init
     call cla_register(key='--input',description='inputfile',kind=cla_char,default='../prm/grid')
     call cla_register(key='-q', description='quiet flag',kind=cla_flag,default='f' )
     call cla_validate
     call cla_get('-q', lquiet)      ! assigns the value .true. to if -q is present
     call cla_get('--input',cfname)  ! assigns input filename to cfname
     ...

## Download

- Grab the [compressed tar file](https://hachi.cee.pdx.edu/fossil/CLAF90/info/tip)

## Contributors

-    Daan van Vugt (d.c.v.vugt ~at~ tue.nl), improved help message (2015-06-24).

-    Eli Ateljevich (Eli.Ateljevich ~at~ water.ca.gov), positional arguments and other enhancements (2015-01-03).

## Acknowledgement

This software was developed with support from the Naval Research Laboratory (Grant #N00173-08-2-C015) and NASA (Grant #NNX13AH06G).
