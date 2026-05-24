import argparse
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys

GENERATED_FILE_EXTENSIONS = [
    ".ll",
    ".opt.ll",
    ".s",
    ".start.o",
    ".o",
    ".elf",
    ".bin",
    ".objdump.txt",
    ".txt",
]
GENERATED_ARTIFACT_SUFFIXES = ["", "_normal"]

COMPILER_BUILD_TARGETS = [
    "clang",
    "opt",
    "llc",
    "llvm-mc",
    "llvm-objcopy",
    "llvm-objdump",
    "lld",
]


def get_base_dir() -> Path:
    return Path(__file__).parent.resolve()


def resolve_executable(name: str, local_bin_dir: Path | None = None) -> str:
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


def resolve_system_llvm_objdump() -> str:
    return resolve_executable("llvm-objdump")


def extract_biggest_objdump_address(objdump_output: str) -> int:
    biggest_address: int | None = None

    for line in objdump_output.splitlines():
        match = re.match(r"^\s*([0-9a-fA-F]+):", line)
        if match is None:
            continue

        address = int(match.group(1), 16)
        if biggest_address is None or address > biggest_address:
            biggest_address = address

    if biggest_address is None:
        sys.exit("Could not find any instruction addresses in llvm-objdump output.")

    return biggest_address


def write_objdump_address_report(
    elf_path: Path, objdump_executable: str, report_path: Path
) -> None:
    completed = subprocess.run(
        [objdump_executable, "-d", "-M", "no-aliases", str(elf_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    biggest_address = extract_biggest_objdump_address(completed.stdout)
    report_path.write_text(f"0x{biggest_address:x}\n")


def compile_test(input_file: str) -> Path:
    base_dir = get_base_dir()
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
    Path(test_dir / input_no_ext).mkdir(parents=True, exist_ok=True)

    ll_path = test_dir / f"{input_no_ext}/{input_no_ext}.ll"
    opt_ll_path = test_dir / f"{input_no_ext}/{input_no_ext}.opt.ll"
    asm_path = test_dir / f"{input_no_ext}/{input_no_ext}.s"
    start_source_path = test_dir / "start.s"
    start_obj_path = test_dir / f"{input_no_ext}/{input_no_ext}.start.o"
    obj_path = test_dir / f"{input_no_ext}/{input_no_ext}.o"
    elf_path = test_dir / f"{input_no_ext}/{input_no_ext}.elf"
    bin_path = test_dir / f"{input_no_ext}/{input_no_ext}.bin"

    # Remove old generated files
    print(f"Cleaning generated files for {input_no_ext}")
    for artifact_suffix in GENERATED_ARTIFACT_SUFFIXES:
        for ext in GENERATED_FILE_EXTENSIONS:
            generated_file = (test_dir / f"{input_no_ext}{artifact_suffix}{ext}").resolve()
            if generated_file.exists():
                generated_file.unlink()

    # .c -> .ll
    print(f"[1/6] Converting {input_file} to {input_no_ext}.ll")

    subprocess.run(
        [
            clang,
            "--target=riscv32",
            "-march=rv32im",
            "-mabi=ilp32",
            "-fsigned-char",
            "-O0",
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
        "-mattr=-zca,+m",
        "-O0",
        str(opt_ll_path),
        "-o",
        str(asm_path),
    ]
    subprocess.run(
        llc_cmd,
        check=True,
    )

    if not start_source_path.is_file():
        sys.exit(f"Startup assembly file doesn't exist: {start_source_path}")

    # Assemble the shared startup file instead of injecting the stub inline.
    print(f"[4/6] Assemble startup object: {start_source_path.name} -> {start_obj_path.name}")
    subprocess.run(
        [
            llvm_mc,
            "-triple=riscv32",
            "-mattr=-zca,+m",
            "-filetype=obj",
            str(start_source_path),
            "-o",
            str(start_obj_path),
        ],
        check=True,
    )

    # .s -> .o
    print(f"[5/6] Assemble object: {asm_path.name} -> {obj_path.name}")
    asm_cmd = [
        llvm_mc,
        "-triple=riscv32",
        "-mattr=-zca,+m",
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
            str(start_obj_path),
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

    return elf_path


def emit_clang_assembly(input_file: str) -> Path:
    base_dir = get_base_dir()
    test_dir = base_dir / "tests"
    compiler_bin_dir = base_dir / "compiler" / "build" / "bin"
    clang = resolve_executable("clang", compiler_bin_dir)
    opt = resolve_executable("opt", compiler_bin_dir)
    llc = resolve_executable("llc", compiler_bin_dir)

    input_path = test_dir / input_file
    if not input_path.is_file():
        sys.exit("Input file doesn't exist.")
    if input_path.suffix != ".c":
        sys.exit("Input file is not a C file.")

    input_no_ext = input_path.stem
    ll_path = test_dir / f"{input_no_ext}/{input_no_ext}_normal.ll"
    opt_ll_path = test_dir / f"{input_no_ext}/{input_no_ext}_normal.opt.ll"
    asm_path = test_dir / f"{input_no_ext}/{input_no_ext}_normal.s"
    start_source_path = test_dir / "start.s"
    start_obj_path = test_dir / f"{input_no_ext}/{input_no_ext}_normal.start.o"
    obj_path = test_dir / f"{input_no_ext}/{input_no_ext}_normal.o"
    elf_path = test_dir / f"{input_no_ext}/{input_no_ext}_normal.elf"

    print(f"[clang] Emit LLVM IR: {input_file} -> {ll_path.name}")
    subprocess.run(
        [
            "clang",
            "--target=riscv32",
            "-march=rv32im",
            "-mabi=ilp32",
            "-fsigned-char",
            "-O0",
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

    print(f"[opt] Optimize IR: {ll_path.name} -> {opt_ll_path.name}")
    subprocess.run(
        [
            "opt",
            "-S",
            "-passes=mem2reg",
            str(ll_path),
            "-o",
            str(opt_ll_path),
        ],
        check=True,
    )

    print(f"[llc] Emit assembly: {opt_ll_path.name} -> {asm_path.name}")
    llc_cmd = [
        "llc",
        "-mtriple=riscv32",
        "-mcpu=generic-rv32",
        "-mattr=-zca,+m",
        "-O0",
        str(opt_ll_path),
        "-o",
        str(asm_path),
    ]
    subprocess.run(
        llc_cmd,
        check=True,
    )

    if not start_source_path.is_file():
        sys.exit(f"Startup assembly file doesn't exist: {start_source_path}")

    print(f"[llvm-mc] Assemble startup object: {start_source_path.name} -> {start_obj_path.name}")
    subprocess.run(
        [
            "llvm-mc",
            "-triple=riscv32",
            "-mattr=-zca,+m",
            "-filetype=obj",
            str(start_source_path),
            "-o",
            str(start_obj_path),
        ],
        check=True,
    )

    print(f"[llvm-mc] Assemble object: {asm_path.name} -> {obj_path.name}")
    subprocess.run(
        [
            "llvm-mc",
            "-triple=riscv32",
            "-mattr=-zca,+m",
            "-filetype=obj",
            str(asm_path),
            "-o",
            str(obj_path),
        ],
        check=True,
    )

    print(f"[lld] Link ELF: {obj_path.name} -> {elf_path.name}")
    subprocess.run(
        [
            "lld",
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
            str(start_obj_path),
            str(obj_path),
            "-o",
            str(elf_path),
        ],
        check=True,
    )

    return elf_path


def run_test(input_file: str | Path) -> None:
    base_dir = get_base_dir()
    simulator_source_path = base_dir / "simulator"
    simulator_build_path = (simulator_source_path / "build").resolve()
    test_dir = (base_dir / "tests").resolve()

    input_path = Path(input_file)
    input_name = input_path.name
    if input_name.endswith(".c"):
        bin_name = f"{input_path.stem}.bin"
    elif input_name.endswith(".bin"):
        bin_name = input_name
    else:
        sys.exit("Input file is not a .c or .bin file.")

    test_case_dir = test_dir / input_path.stem
    input_file_path = (test_case_dir / bin_name).resolve()
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

    output_path = test_case_dir / f"{input_path.stem}.txt"
    with output_path.open("w") as output_file:
        subprocess.run(
            [str(simulator_executable), str(input_file_path)],
            check=True,
            stdout=output_file,
            stderr=subprocess.STDOUT,
            text=True,
        )


def get_test_files():
    test_dir = (Path(__file__).parent / "tests").resolve()
    return test_dir.glob("*.c")


def normalize_c_test_name(name: str) -> str:
    input_name = Path(name).name
    if input_name.endswith(".c"):
        return input_name
    if input_name.endswith(".bin"):
        return f"{Path(input_name).stem}.c"
    return f"{input_name}.c"


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--simulator", help="Enable simulator running.", action="store_true"
    )
    parser.add_argument(
        "-f",
        "--file",
        nargs="+",
        help="Specify test file(s) to run.",
    )
    args = parser.parse_args()

    # Compile all test files
    base_dir = get_base_dir()
    subprocess.run(
        ["cmake", "--build", "compiler/build", "--target", *COMPILER_BUILD_TARGETS],
        check=True,
        cwd=str(base_dir),
    )

    all_test_files = list(get_test_files())
    all_test_names = {file.name for file in all_test_files}

    if args.file:
        selected_test_names = [normalize_c_test_name(name) for name in args.file]
        missing_tests = [
            name for name in selected_test_names if name not in all_test_names
        ]
        if missing_tests:
            missing = ", ".join(missing_tests)
            sys.exit(f"Requested test file(s) not found in tests/: {missing}")
    else:
        selected_test_names = [file.name for file in all_test_files]

    tagged_elf_paths = {}
    normal_elf_paths = {}

    for test_name in selected_test_names:
        tagged_elf_paths[test_name] = compile_test(test_name)

    for test_name in selected_test_names:
        normal_elf_paths[test_name] = emit_clang_assembly(test_name)

    tagged_objdump = resolve_executable(
        "llvm-objdump", base_dir / "compiler" / "build" / "bin"
    )
    system_objdump = resolve_system_llvm_objdump()

    for test_name in selected_test_names:
        test_case_dir = (base_dir / "tests" / Path(test_name).stem).resolve()
        tagged_report_path = test_case_dir / f"{Path(test_name).stem}.objdump.txt"
        normal_report_path = test_case_dir / f"{Path(test_name).stem}_normal.objdump.txt"

        write_objdump_address_report(
            tagged_elf_paths[test_name], tagged_objdump, tagged_report_path
        )
        write_objdump_address_report(
            normal_elf_paths[test_name], system_objdump, normal_report_path
        )

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

        for test_name in selected_test_names:
            run_test(test_name)
