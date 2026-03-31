import subprocess
import argparse
import os
import pathlib
import sys


def compile_test(input_file, assembly=False, tagged=False):
    # Remove old generated files
    print("Cleaning up old generated files")
    test_dir = pathlib.Path(__file__).parent / "tests"
    for ext in [".ll", ".opt.ll", ".o", ".bin", ".s"]:
        file = (test_dir / f"{input_file}.{ext}").resolve()
        if file.exists():
            file.unlink()

    input_path = test_dir / input_file
    if not input_path.is_file():
        sys.exit("Input file doesn't exist.")

    if not input_file.endswith(".c"):
        sys.exit("Input file is not a C file.")

    input_no_ext = input_file.replace(".c", "")

    base_dir = pathlib.Path(__file__).parent.resolve()
    compiler_bin_dir = base_dir / "compiler" / "build" / "bin"

    # .c -> .ll
    print(f"Converting {input_file} to {input_no_ext}.ll")
    subprocess.run(
        [
            "clang",
            "--target=riscv32",
            "-march=rv32i",
            "-mabi=ilp32",
            "-O0",
            "-fomit-frame-pointer",
            "-Xclang",
            "-disable-O0-optnone",
            "-S",
            "-emit-llvm",
            str(input_path),
            "-o",
            str(test_dir / f"{input_no_ext}.ll"),
        ],
        check=True,
    )

    # Tag store instructions if requested
    if tagged:
        # .ll -> .opt.ll
        print(
            f"Converting {input_file}.ll to {input_no_ext}.opt.ll with tagged store instructions"
        )
        subprocess.run(
            [
                str(compiler_bin_dir / "opt"),
                "-S",
                "-passes=mem2reg",
                "-mattr=+tagged-mem-stores",
                str(test_dir / f"{input_no_ext}.ll"),
                "-o",
                str(test_dir / f"{input_no_ext}.opt.ll"),
            ],
            check=True,
        )
    else:
        # .ll -> .opt.ll
        print(f"Converting {input_no_ext}.ll to {input_no_ext}.opt.ll")
        subprocess.run(
            [
                str(compiler_bin_dir / "opt"),
                "-S",
                "-passes=mem2reg",
                str(test_dir / f"{input_no_ext}.ll"),
                "-o",
                str(test_dir / f"{input_no_ext}.opt.ll"),
            ],
            check=True,
        )

    # .opt.ll -> .o
    print(f"Converting {input_no_ext}.opt.ll to {input_no_ext}.o")
    subprocess.run(
        [
            str(compiler_bin_dir / "llc"),
            "-mtriple=riscv32",
            "-mcpu=generic-rv32",
            "-mattr=-c",
            "-mattr=-zca",
            "-O0",
            "-filetype=obj",
            str(test_dir / f"{input_no_ext}.opt.ll"),
            "-o",
            str(test_dir / f"{input_no_ext}.o"),
        ],
        check=True,
    )

    # .o -> .bin
    print(f"Converting {input_no_ext}.o to {input_no_ext}.bin")
    subprocess.run(
        [
            str(compiler_bin_dir / "llvm-objcopy"),
            "-O",
            "binary",
            str(test_dir / f"{input_no_ext}.o"),
            str(test_dir / f"{input_no_ext}.bin"),
        ],
        check=True,
    )

    # Generate assembly file if requested
    if assembly:
        # .opt.ll -> .s
        print(f"Generating assembly file from {input_file}")
        subprocess.run(
            [
                str(compiler_bin_dir / "llc"),
                "-mtriple=riscv32",
                "-mcpu=generic-rv32",
                "-mattr=-c",
                "-mattr=-zca",
                "-O0",
                str(test_dir / f"{input_no_ext}.opt.ll"),
                "-o",
                str(test_dir / f"{input_no_ext}.s"),
            ],
            check=True,
        )


def run_test(input_file):
    base_dir = pathlib.Path(__file__).parent.resolve()
    simulator_source_path = base_dir / "simulator"
    simulator_build_path = (simulator_source_path / "build").resolve()
    test_dir = (base_dir / "tests").resolve()

    input_path = pathlib.Path(input_file)
    input_name = input_path.name
    if input_name.endswith(".c"):
        bin_name = f"{input_path.stem}.bin"
    elif input_name.endswith(".bin"):
        bin_name = input_name
    else:
        sys.exit("Input file is not a .c or .bin file.")

    input_file_path = (test_dir / bin_name).resolve()
    if not input_file_path.is_file():
        sys.exit(f"Compiled binary doesn't exist: {input_file_path}")

    # Configure once if needed, then build.
    if not (simulator_build_path / "CMakeCache.txt").is_file():
        subprocess.run(
            [
                "cmake",
                "-S",
                str(simulator_source_path),
                "-B",
                str(simulator_build_path),
            ],
            check=True,
        )

    subprocess.run(["cmake", "--build", str(simulator_build_path)], check=True)

    simulator_candidates = [
        simulator_build_path / "simulator",
        simulator_build_path / "simulator.exe",
        simulator_build_path / "Debug" / "simulator.exe",
        simulator_build_path / "Release" / "simulator.exe",
    ]
    simulator_executable = next((p for p in simulator_candidates if p.exists()), None)
    if simulator_executable is None:
        sys.exit(f"Could not find simulator executable in: {simulator_build_path}")

    subprocess.run([str(simulator_executable), str(input_file_path)], check=True)


def get_test_files():
    test_dir = (pathlib.Path(__file__).parent / "tests").resolve()
    return test_dir.glob("*.c")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--assembly", help="generates assembly file", action="store_true"
    )
    parser.add_argument(
        "-t", "--tagged", help="Uses tagged store instructions", action="store_true"
    )
    args = parser.parse_args()

    # Compile all test files
    test_files = list(get_test_files())
    for file in test_files:
        compile_test(file.name, args.assembly, args.tagged)

    # Run the test files in the simulator
    for file in test_files:
        run_test(file)
