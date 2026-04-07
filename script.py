import subprocess
import argparse
import os
import pathlib
import shutil
import sys


def prepend_start_stub(asm_path: pathlib.Path):
    original = asm_path.read_text()

    start_stub = """\
\t.globl\t_start
\t.p2align\t2
\t.type\t_start,@function
_start:
\tcall\tmain
\tebreak

"""
    asm_path.write_text(start_stub + original)


def resolve_executable(name: str, local_bin_dir: pathlib.Path | None = None) -> str:
    candidates = [name]
    if os.name == "nt" and not name.lower().endswith(".exe"):
        candidates.insert(0, f"{name}.exe")

    if local_bin_dir is not None:
        for candidate in candidates:
            local_path = local_bin_dir / candidate
            if local_path.is_file():
                return str(local_path)

    for candidate in candidates:
        found = shutil.which(candidate)
        if found:
            return found

    search_hint = f" and {local_bin_dir}" if local_bin_dir else ""
    sys.exit(f"Could not find executable '{name}' in PATH{search_hint}.")


def compile_test(input_file, tagged=False):
    base_dir = pathlib.Path(__file__).parent.resolve()
    test_dir = base_dir / "tests"
    compiler_bin_dir = base_dir / "compiler" / "build" / "bin"
    clang = resolve_executable("clang", compiler_bin_dir)
    opt = resolve_executable("opt", compiler_bin_dir)
    llc = resolve_executable("llc", compiler_bin_dir)
    llvm_mc = resolve_executable("llvm-mc", compiler_bin_dir)
    lld = resolve_executable("lld", compiler_bin_dir)
    llvm_objcopy = resolve_executable("llvm-objcopy", compiler_bin_dir)

    input_path = test_dir / input_file
    if not input_path.is_file():
        sys.exit("Input file doesn't exist.")
    if input_path.suffix != ".c":
        sys.exit("Input file is not a C file.")

    input_no_ext = input_path.stem
    ll_path = test_dir / f"{input_no_ext}.ll"
    opt_ll_path = test_dir / f"{input_no_ext}.opt.ll"
    asm_path = test_dir / f"{input_no_ext}.s"
    obj_path = test_dir / f"{input_no_ext}.o"
    elf_path = test_dir / f"{input_no_ext}.elf"
    bin_path = test_dir / f"{input_no_ext}.bin"

    tagged_mattr_flag = "--mattr=+tagged-mem-stores"

    # Remove old generated files
    print(f"Cleaning generated files for {input_no_ext}")
    for ext in [".ll", ".opt.ll", ".o", ".bin", ".s", ".elf"]:
        file = (test_dir / f"{input_no_ext}{ext}").resolve()
        if file.exists():
            file.unlink()

    # .c -> .ll
    print(f"[1/6] LLVM IR: {input_file} -> {ll_path.name}")
    subprocess.run(
        [
            clang,
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
            str(ll_path),
        ],
        check=True,
    )

    # .ll -> .opt.ll
    if tagged:
        print(
            f"[2/6] Optimize IR (tagged stores): {ll_path.name} -> {opt_ll_path.name}"
        )
        subprocess.run(
            [
                opt,
                "-S",
                "-passes=mem2reg",
                tagged_mattr_flag,
                str(ll_path),
                "-o",
                str(opt_ll_path),
            ],
            check=True,
        )
    else:
        print(f"[2/6] Optimize IR: {ll_path.name} -> {opt_ll_path.name}")
        subprocess.run(
            [
                opt,
                "-S",
                "-passes=mem2reg",
                str(ll_path),
                "-o",
                str(opt_ll_path),
            ],
            check=True,
        )

    # .opt.ll -> .s
    print(f"[3/6] Emit assembly: {opt_ll_path.name} -> {asm_path.name}")
    llc_cmd = [
        llc,
        "-mtriple=riscv32",
        "-mcpu=generic-rv32",
        "-mattr=-c",
        "-mattr=-zca",
        "-O0",
        str(opt_ll_path),
        "-o",
        str(asm_path),
    ]
    if tagged:
        llc_cmd.insert(5, tagged_mattr_flag)
    subprocess.run(
        llc_cmd,
        check=True,
    )

    # Add bare-metal entry symbol expected by the simulator.
    print(f"[4/6] Inject startup stub into {asm_path.name}")
    prepend_start_stub(asm_path)

    # .s -> .o
    print(f"[5/6] Assemble object: {asm_path.name} -> {obj_path.name}")
    asm_mattr = "-mattr=+tagged-mem-stores,-c,-zca" if tagged else "-mattr=-c,-zca"
    asm_cmd = [
        llvm_mc,
        "-triple=riscv32",
        asm_mattr,
        "-filetype=obj",
        str(asm_path),
        "-o",
        str(obj_path),
    ]
    subprocess.run(
        asm_cmd,
        check=True,
    )

    # .o -> .elf
    print(f"[6/6] Link ELF: {obj_path.name} -> {elf_path.name}")
    subprocess.run(
        [
            lld,
            "-flavor",
            "gnu",
            "-m",
            "elf32lriscv",
            "-e",
            "_start",
            "-Ttext",
            "0x0",
            "--image-base",
            "0x0",
            str(obj_path),
            "-o",
            str(elf_path),
        ],
        check=True,
    )

    # .elf -> .bin
    print(f"Export binary image: {elf_path.name} -> {bin_path.name}")
    subprocess.run(
        [
            llvm_objcopy,
            "-O",
            "binary",
            str(elf_path),
            str(bin_path),
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

    simulator_names = (
        ["simulator.exe", "simulator"]
        if os.name == "nt"
        else ["simulator", "simulator.exe"]
    )
    simulator_candidates = (
        [simulator_build_path / name for name in simulator_names]
        + [simulator_build_path / "Debug" / name for name in simulator_names]
        + [simulator_build_path / "Release" / name for name in simulator_names]
    )
    simulator_executable = next((p for p in simulator_candidates if p.exists()), None)
    if simulator_executable is None:
        sys.exit(f"Could not find simulator executable in: {simulator_build_path}")

    output_path = test_dir / f"{input_path.stem}.txt"
    with output_path.open("w") as output_file:
        subprocess.run(
            [str(simulator_executable), str(input_file_path)],
            check=True,
            stdout=output_file,
            stderr=subprocess.STDOUT,
            text=True,
        )


def get_test_files():
    test_dir = (pathlib.Path(__file__).parent / "tests").resolve()
    return test_dir.glob("*.c")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--tagged", help="Uses tagged store instructions", action="store_true"
    )
    parser.add_argument(
        "-s", "--simulator", help="Enable simulator running.", action="store_true"
    )
    args = parser.parse_args()

    # Compile all test files
    base_dir = pathlib.Path(__file__).parent.resolve()
    subprocess.run(
        [
            "cmake",
            "--build",
            "compiler/build",
            "--target",
            "opt",
            "llc",
            "llvm-mc",
            "lld",
            "llvm-objcopy",
            "llvm-objdump",
        ],
        check=True,
        cwd=str(base_dir),
    )

    test_files = list(get_test_files())
    for file in test_files:
        compile_test(file.name, args.tagged)

    # Run the test files in the simulator
    if args.simulator:
        simulator_source_path = base_dir / "simulator"
        simulator_build_path = (simulator_source_path / "build").resolve()

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
        for file in test_files:
            run_test(file)
