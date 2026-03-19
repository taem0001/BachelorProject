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

    input = args.input

    base_dir = pathlib.Path(__file__).parent.resolve()
    input_path = os.path.join(base_dir, input)
    if not os.path.isfile(input_path):
        sys.exit("Input file doesn't exist.")

    if not input.endswith(".c"):
        sys.exit("Input file is not a C file.")

    input_no_ext = input.replace(".c", "")

    print(f"Converting {input} to {input_no_ext}.ll")
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
            f"{input}",
            "-o",
            f"{input_no_ext}.ll",
        ]
    )

    print(f"Converting {input_no_ext}.ll to {input_no_ext}.opt.ll")
    subprocess.run(
        [
            "./compiler/build/bin/opt",
            "-S",
            "-passes=mem2reg",
            f"{input_no_ext}.ll",
            "-o",
            f"{input_no_ext}.opt.ll",
        ]
    )

    print(f"Converting {input_no_ext}.opt.ll to {input_no_ext}.o")
    subprocess.run(
        [
            "./compiler/build/bin/llc",
            "-mtriple=riscv32",
            "-O0",
            "-filetype=obj",
            f"{input_no_ext}.opt.ll",
            "-o",
            f"{input_no_ext}.o",
        ]
    )

    print(f"Converting {input_no_ext}.o to {input_no_ext}.bin")
    subprocess.run(
        [
            "./compiler/build/bin/llvm-objcopy",
            "-O",
            "binary",
            f"{input_no_ext}.o",
            f"{input_no_ext}.bin",
        ]
    )

    if args.assembly:
        print(f"Generating assembly file from {input}")
        subprocess.run(
            [
                "./compiler/build/bin/llc",
                "-mtriple=riscv32",
                "-O0",
                f"{input_no_ext}.opt.ll",
                "-o",
                f"{input_no_ext}.s",
            ]
        )
