from pathlib import Path
import asyncio
import subprocess
import sys
import concurrent.futures
import itertools

__version__ = "1.2.0"


def fortran_test_generator() -> dict[str, str]:
    """
    provides simple code block elements to test compiler feature level
    """

    tests = {
        "minimal": "end",
        "f2003ieee": "use, intrinsic :: ieee_arithmetic; print *, ieee_next_after(0.,0.); end",
        "f2003utf8": "use, intrinsic :: ieee_arithmetic, only ; print *, ieee_next_after(0.,0.), end",
        "f2008rank15": "integer :: a(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1); print*,rank(a);end",
        "f2008contiguous": "print*,is_contiguous([0,0]); end",
        "f2018errorstop": "character :: a; error stop a; end",
        "f2008kind": "use, intrinsic :: iso_fortran_env; print *, huge(0._real128); end",
        "f2008version": "use, intrinsic :: iso_fortran_env; print *, compiler_version(); end",
        "f2008block": "block; a=0.; end block; end",
        "f2018randominit": "call random_init(.false., .false.); end",
        "f2018properties": "complex :: z; print *,z%re,z%im,z%kind; end",
        "f2023rank": "real, rank(2) :: a; end",
        "f2023real16": "use, intrinsic :: iso_fortran_env, only: real16; end",
        "f2023ternary": "real :: a, v; v = ( a > 0.0 ? a : 0.0); end",
        "f2023tokenize": "intrinsic :: tokenize; end",
        "f2023enum": """enumeration type :: colour
enumerator :: red, orange, green
end enumeration type
end program"""
    }

    return tests


def write_tests(temp_dir: Path) -> set[Path]:
    tests = fortran_test_generator()

    src_files = []
    for name, src in tests.items():
        src_files.append(temp_dir / (name + ".f90"))
        src_files[-1].write_text(src)

    return set(src_files)


async def arbiter(
    compiler: str, src_files: set[Path], Nrun: int, verbose: bool
) -> dict[str, bool]:
    """
    example tests for compilers

    in real use, instead of printing results, we would perhaps return dict
    with compiler capabilites as suitable for main program.
    """

    futures = []
    for _ in range(Nrun):  # just to run the tests many times
        for src_file in src_files:
            futures.append(fortran_compiler_ok(compiler, src_file, verbose))

    results = await asyncio.gather(*futures)

    return dict(results)


async def fortran_compiler_ok(
    compiler: str, src_file: Path, verbose: bool = False
) -> tuple[str, bool]:
    """check that Fortran compiler is able to compile a basic program"""

    cmd = [compiler, str(src_file)]
    # print(' '.join(cmd))
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    # print(stdout.decode('utf8'))
    errmsg = stderr.decode("utf8")
    if verbose and errmsg:
        print(stderr.decode("utf8"), file=sys.stderr)

    return src_file.stem, proc.returncode == 0


def fortran_compiler_ok_sync(compiler: str, src_file: Path) -> tuple[str, bool]:
    """check that Fortran compiler is able to compile a basic program"""

    ret = subprocess.run([compiler, str(src_file)], stderr=subprocess.DEVNULL)

    return src_file.stem, ret.returncode == 0


def fortran_compiler_threadpool(compiler: str, src_files: set[Path], Nrun: int) -> dict[str, bool]:
    """
    ThreadPool for parallel compilation
    """

    for _ in range(Nrun):  # just to run the tests many times
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(fortran_compiler_ok_sync, itertools.repeat(compiler), src_files)

    return dict(results)


def fortran_compiler_processpool(
    compiler: str, src_files: set[Path], Nrun: int
) -> dict[str, bool]:
    """
    ProcessPoolExecutor for parallel compilation
    """

    for _ in range(Nrun):  # just to run the tests many times
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(fortran_compiler_ok_sync, itertools.repeat(compiler), src_files)

    return dict(results)
