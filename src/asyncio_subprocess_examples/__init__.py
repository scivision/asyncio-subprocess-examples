from __future__ import annotations
import os
import asyncio
import subprocess
import logging
import tempfile
import sys

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
        "2023rank": "real, rank(2) :: a; end"
    }

    return tests


async def arbiter(compiler: str, Nrun: int, verbose: bool) -> dict[str, bool]:
    """
    example tests for compilers

    in real use, instead of printing results, we would perhaps return dict
    with compiler capabilites as suitable for main program.
    """

    tests = fortran_test_generator()

    futures = []
    for _ in range(Nrun):  # just to run the tests many times
        for testname, testsrc in tests.items():
            futures.append(fortran_compiler_ok(compiler, testname, testsrc, verbose))

    results = await asyncio.gather(*futures)

    return dict(results)


async def fortran_compiler_ok(
    compiler: str, name: str, src: str, verbose: bool = False
) -> tuple[str, bool]:
    """check that Fortran compiler is able to compile a basic program"""

    with tempfile.NamedTemporaryFile("w", suffix=".f90", delete=False) as f:
        f.write(src)

    logging.debug(f"testing {compiler} with source: {src}")
    cmd = [compiler, f.name]
    # print(' '.join(cmd))
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    # this and delete=False is necessary due to Windows no double-open file limitation
    os.unlink(f.name)

    # print(stdout.decode('utf8'))
    errmsg = stderr.decode("utf8")
    if verbose and errmsg:
        print(stderr.decode("utf8"), file=sys.stderr)

    return name, proc.returncode == 0


def fortran_compiler_ok_sync(compiler: str, name: str, src: str) -> tuple[str, bool]:
    """check that Fortran compiler is able to compile a basic program"""

    with tempfile.NamedTemporaryFile("w", suffix=".f90", delete=False) as f:
        f.write(src)

    logging.debug(f"testing {compiler} with source: {src}")
    cmd = [compiler, f.name]
    ret = subprocess.run(cmd, stderr=subprocess.DEVNULL)

    # this and delete=False is necessary due to Windows no double-open file limitation
    os.unlink(f.name)

    return name, ret.returncode == 0
