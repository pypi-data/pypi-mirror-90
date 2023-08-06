Quick Overview
==============

This document outlines the usage of the `make`-based build "system".

## Quick start

The code can be built as follows:

`$ make -f Makefile.take2 -j4`

(the standard make option `-j4` enables parallel builds with up to four
processes; change the number four to match the resources available to you.)

By default, this builds the "debug" configuration using the GCC toolchain
(i.e., using `gfortran`). A different configuration may be selected via the
`BUILD` value:

`$ make -f Makefile.take2 -j4 BUILD=release`

The toolchain can be changed via the `TOOLCHAIN` value:

`$ make -f Makefile.take2 -j4 TOOLCHAIN=intel`

The aim is to support at least the following build configurations for each
toolchain:

 - `debug`: unoptimized build with debug information and possibly with 
   additional run-time checks. Mostly relevant for code development.
 - `release`: fully optimized build sans debug information.
 - `relWithDbgInfo`: fully optimized build with debug information.

At the time of writing, two toolchains are supported:

 - `gcc`: using the GNU Compiler Collection (i.e., `gfortran` et al.)
 - `intel`: using the Intel compilers (i.e., `ifort` et al.)

All values are case sensitive. 


Built files are placed in the following output directories:
  - `bin/`
  - `lib/`
The names of these files (binaries and libraries) include a suffix
`-<toolchain>-<build>`, corresponding to the `TOOLCHAIN` and `BUILD` settings
that were selected.

Temporary files are placed in the directory `build/<toolchain>-<build>/`. 
All fortran module files are placed in `include/<toolchain>-<build>`.


Additionally, the following two options may be passed to `make`:

  - `VERBOSE=1`: prints the full commands that are executed by the build
  - `NOCOLOR=1`: disables the colorization of the output by make (#)

(#): Some tools (e.g., gfortran) may still include color in their output,
regardless of this setting.


To generate a list of the processed makefiles, use `make overview`. This
displays a list of all included sub-makefiles and their locations. Support
files (i.e., the build system functions located in `defs/`) are excluded from
this list.

## Makefiles

There are three different types of makefiles present:
 - Build definitions
 - Build configuration
 - Build system components

Build definitions contain information on how to build source code into the
final products. Build configuration define properties of each build, i.e., what
tools to use, what flags should be enabled, and where to find external
libraries and sources. Both build definitions and build configurations need to
be updated during development. The build system components instead hold the
system together, and (hopefully) do not need to be changed.

### Build configuration

Build configuration is contained in the following files:

 - `defs/variants/$(TOOLCHAIN)-$(BUILD).make`
 - `defs/localcfg/<machine-name>.make`
 - `usercfg.make`

Additionally, build definitions can add/override certain settings locally. See
next section.

Each combination of toolchain and build configuration is referred to as a 
variant. Each variant is defined by a single file in the `defs/variants/`
directory. Creating a new variant is as simple as creating the corresponding
file in the variants directory.

Machine-dependent settings should be placed in the `defs/localcfg` directory.
The settings are loaded based on the hostname (as reported by `hostname -f`) of
the machine where `make` is run. For example, when running on the machine
`r000u05g02.marconi.cineca.it`, the build will attempt to load the following
files

  - `defs/localcfg/r000u05g02.marconi.cineca.it.make`
  - `defs/localcfg/marconi.cineca.it.make`
  - `defs/localcfg/cineca.it.make`
  - `defs/localcfg/it.make`

in the above order. It is recommended that `localcfg` files are checked into
source control.

Finally, a `usercfg.make` is loaded from the root directory (i.e., the parent
of the `defs/` directory). This file can be used to override settings on a
per-user level. The `usercfg.make` *should not* be checked into source control.

Configuration files may not contain build rules, but must instead only define
variables and macros.

### Build definitions

Build definitions define the inputs and outputs of the build. These start with
the entry points (e.g., top-level `Makefile`s), and include any number of sub-
makefiles. 

A project is defined for each target:

```
$(call SUBPROJECT_open,<name>,<targetType>)
...
$(call SUBPROJECT_close)
```

`<name>` is a user-selected unique name for the "project". `<targetType>`
is one of the following
  - `staticlib` (static library, `lib<name>-<variant>.a`)
  - `app` (executable, `<name>-<variant>.exe`)

All of the following commands must be issued between the `open`/`close` pair
above (i.e., in the location of `...`).
 
A project may depend on other projects; these dependencies are defined via
`SUBPROJECT_depend`:

```
$(call SUBPROJECT_depend,<nameA> <nameB>)
```

The current project now depends on the projects named `<nameA>` and `<nameB>`.
One or more projects may be listed.  Typically, a `app` project will depend on
one or more `staticlibrary` projects.

Additional flags to the linker may be specified using

```
$(call SUBPROJECT_set_linkflags, <toolchain>, <flags...> )
``` 

The flags `<flags...>` will be passed to the linking stage as-is when built with
the selected `<toolchain>`. For example

```
$(call SUBPROJECT_set_linkflags, gcc, -lgcc_only_library )
$(call SUBPROJECT_set_linkflags, intel, -lintel_only_library )
```

will append `-lgcc_only_library` to the linker's command line when building with 
the `gcc` toolchain, and `-lintel_only_library` when building with the `intel` 
toolchain.


Sources may be added via `SUBPROJECT_add`; however, this command assumes that
full (absolute) paths are used. In order to simplify the use of local sources
(i.e., with paths relative to the current makefile), a number of "local" 
commands are provided.

The following example adds the files `a.f90` and `b.f90` which are in the same
directory as the current makefile.

```
$(call SUBPROJECT_reset_local)
$(call SUBPROJECT_set_local_dir_here)
$(call LOCAL_add, a.f90 b.f90)
```

WARNING: using `include <file>.make` in the _same file_ may prior to the 
`SUBPROJECT_set_local_dir_here` command may confuse that command. 
TODO-workaround!

These commands may be issued multiple times in each project. Therefore it is
important to use `SUBPROJECT_reset_local`, which resets any local settings (as
set by `SUBPROJECT_set_local_*`). `SUBPROJECT_set_local_dir_here` tells the
build system that any sources referred to in the following commands use paths
relative to the current makefile's location. `LOCAL_add` finally adds the
source files.

Additional local commands include:
  - `SUBPROJECT_set_local_fflags, <toolchain>, <flags...>`
  - `LOCAL_mod_dep, <source>, <module names...>`
  - `LOCAL_mod_out, <source>, <module names...>`

`SUBPROJECT_set_local_fflags` may be used to add the fortran compiler flags
`<flags...>` to the source files added in the following `LOACL_add` commands.
Compiler flags, like linker flags, are defined separately for each toolchain.

`LOCAL_mod_dep` specifies a list of modules that the source file `<source>`
depends upon. For example,

```
$(call LOCAL_mod_dep, a.f90, b.mod c.mod)
```

ensures that the sources producing `b.mod` and `c.mod` are built before
attempting to build `a.f90`. By default, the system assumes that a source file
named `foo.f90` will produce a module `foo.mod`. Occasionally this is not the
case; produced modules can therefore be specified using the command
`LOCAL_mod_out` as follows:

```
$(call LOCAL_mod_out, vexing.f90, unrelated.mod modules.mod)
```

NOTE: All file names are case-sensitive. In particular, module files should
always use lower-case names, as the output modules files created by the fortran
compilers use lower-case names.

WARNING: all modules from all projects are placed into the same directory. Two
modules with the same name may therefore result in excessive "fun".

### Build System components

All build system components are located in `defs/` and have the extension
`*.make`. Developers entertaining thoughts of inspecting these parts should be
prepared to abandon any semblance of sanity. (Make is not a pretty language.)


## TODO-Title




#%EOF vim:syntax=markdown:spell:
