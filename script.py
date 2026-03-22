import subprocess
import argparse
import os
import pathlib
import sys


if __name__ == "__main__":
    # Remove old generated files
    print("Cleaning up old generated files...")
    for ext in [".ll", ".opt.ll", ".o", ".bin", ".s"]:
        for file in pathlib.Path(__file__).parent.glob(f"*{ext}"):
            file.unlink()

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input test file")
    parser.add_argument(
        "-a", "--assembly", help="generates assembly file", action="store_true"
    )
    parser.add_argument(
        "-t", "--tagged", help="Uses tagged store instructions", action="store_true"
    )
    args = parser.parse_args()

    input_file = args.input

    base_dir = pathlib.Path(__file__).parent.resolve()
    input_path = base_dir / input_file
    if not input_path.is_file():
        sys.exit("Input file doesn't exist.")

    if not input_file.endswith(".c"):
        sys.exit("Input file is not a C file.")

    input_no_ext = input_file.replace(".c", "")

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
            str(base_dir / f"{input_no_ext}.ll"),
        ],
        check=True,
    )

    # Tag store instructions if requested
    if args.tagged:
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
                str(base_dir / f"{input_no_ext}.ll"),
                "-o",
                str(base_dir / f"{input_no_ext}.opt.ll"),
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
                str(base_dir / f"{input_no_ext}.ll"),
                "-o",
                str(base_dir / f"{input_no_ext}.opt.ll"),
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
            str(base_dir / f"{input_no_ext}.opt.ll"),
            "-o",
            str(base_dir / f"{input_no_ext}.o"),
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
            str(base_dir / f"{input_no_ext}.o"),
            str(base_dir / f"{input_no_ext}.bin"),
        ],
        check=True,
    )

    # Generate assembly file if requested
    if args.assembly:
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
                str(base_dir / f"{input_no_ext}.opt.ll"),
                "-o",
                str(base_dir / f"{input_no_ext}.s"),
            ],
            check=True,
        )
