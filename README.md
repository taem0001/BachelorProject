# BachelorProject

Bachelor project repository for compiling C test programs to RISC-V binaries and optionally running them in a simulator.

The project ties together two submodules:

- `compiler` — custom LLVM/Clang-based compiler toolchain
- `simulator` — simulator used to execute generated binaries

The top-level `script.py` automates the build, compile, comparison, and optional simulation workflow for the test programs in `tests/`.

## Repository structure

```text
BachelorProject/
├── compiler/      # Compiler submodule
├── simulator/     # Simulator submodule
├── tests/         # C test programs and generated outputs
├── script.py      # Main automation script
└── .gitmodules    # Submodule configuration
```

## Requirements

Make sure the following tools are installed:

- Python 3
- CMake
- A C/C++ build toolchain
- LLVM tools available on `PATH` for the reference build:
  - `clang`
  - `opt`
  - `llc`
  - `llvm-mc`
  - `llvm-objdump`
  - `lld`

The custom compiler is expected to be built in:

```text
compiler/build
```

The simulator is expected to be built in:

```text
simulator/build
```

## Setup

Clone the repository with submodules:

```bash
git clone --recurse-submodules https://github.com/taem0001/BachelorProject.git
cd BachelorProject
```

If the repository has already been cloned without submodules, initialize them with:

```bash
git submodule update --init --recursive
```

## Build the compiler

Create and build the compiler build directory:

```bash
cmake -S compiler -B compiler/build
cmake --build compiler/build
```

The automation script also builds the required compiler targets before running tests.

## Running tests

To compile all C test files in `tests/`, run:

```bash
python3 script.py
```

The script will:

1. Build the required compiler tools from `compiler/build`
2. Find all `.c` files in `tests/`
3. Compile each test to LLVM IR
4. Run the `mem2reg` optimization pass
5. Emit RISC-V assembly
6. Assemble and link an ELF file
7. Export a raw binary file
8. Generate objdump address reports
9. Also generate a reference `_normal` version using the system LLVM tools

Generated files are placed in per-test directories under `tests/`.

For example, running the script on `example.c` will create output files similar to:

```text
tests/example/
├── example.ll
├── example.opt.ll
├── example.s
├── example.start.o
├── example.o
├── example.elf
├── example.bin
├── example.objdump.txt
├── example_normal.ll
├── example_normal.opt.ll
├── example_normal.s
├── example_normal.start.o
├── example_normal.o
├── example_normal.elf
└── example_normal.objdump.txt
```

## Running a specific test

Use the `-f` or `--file` option to run one or more specific tests:

```bash
python3 script.py -f test_file.c
```

You can also pass multiple files:

```bash
python3 script.py -f test1.c test2.c test3.c
```

The `.c` extension is optional:

```bash
python3 script.py -f test_file
```

## Running tests in the simulator

Use the `-s` or `--simulator` flag to also build the simulator and run the generated binaries:

```bash
python3 script.py --simulator
```

Or for a specific test:

```bash
python3 script.py --simulator --file test_file.c
```

Simulator output is written to a `.txt` file in the test’s generated output directory.

For example:

```text
tests/test_file/test_file.txt
```

## Test files

Test files should be placed directly in the `tests/` directory and must use the `.c` extension.

Example:

```text
tests/add.c
tests/branch.c
tests/memory.c
```

The script automatically discovers all `.c` files in this directory unless specific files are provided with `--file`.

## Startup assembly

The script expects a shared startup assembly file at:

```text
tests/start.s
```

This file is assembled and linked with each compiled test program.

## Cleaning generated files

The script automatically removes old generated files for each test before recompiling it.

Generated files include:

- `.ll`
- `.opt.ll`
- `.s`
- `.start.o`
- `.o`
- `.elf`
- `.bin`
- `.objdump.txt`
- `.txt`

## Useful commands

Compile all tests:

```bash
python3 script.py
```

Compile one test:

```bash
python3 script.py -f test_file.c
```

Compile and run all tests in the simulator:

```bash
python3 script.py -s
```

Compile and run one test in the simulator:

```bash
python3 script.py -s -f test_file.c
```

## Notes

- The custom compiler tools are resolved from `compiler/build/bin` when available.
- The reference `_normal` build uses LLVM tools from the system `PATH`.
- The simulator executable is searched for in `simulator/build`, including common `Debug` and `Release` subdirectories.
