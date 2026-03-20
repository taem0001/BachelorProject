import subprocess
import argparse
import os
import pathlib
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input test file")
    parser.add_argument(
        "-a", "--assembly", help="generates assembly file", action="store_true"
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
            "-O0",
            "-fomit-frame-pointer",
            "-Xclang",
            "-disable-O0-optnone",
            "-S",
            "-emit-llvm",
            str(input_path),
            "-o",
            str(base_dir / f"{input_no_ext}.ll"),
        ]
    )

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
        ]
    )

    # .opt.ll -> .o
    print(f"Converting {input_no_ext}.opt.ll to {input_no_ext}.o")
    subprocess.run(
        [
            str(compiler_bin_dir / "llc"),
            "-mtriple=riscv32",
            "-O0",
            "-filetype=obj",
            str(base_dir / f"{input_no_ext}.opt.ll"),
            "-o",
            str(base_dir / f"{input_no_ext}.o"),
        ]
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
        ]
    )

    if args.assembly:
        # .opt.ll -> .s
        print(f"Generating assembly file from {input_file}")
        subprocess.run(
            [
                str(compiler_bin_dir / "llc"),
                "-mtriple=riscv32",
                "-O0",
                str(base_dir / f"{input_no_ext}.opt.ll"),
                "-o",
                str(base_dir / f"{input_no_ext}.s"),
            ]
        )
