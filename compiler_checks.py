#!/usr/bin/env python
"""
Python >= 3.5
"""
import sys
import shutil
import os
import asyncio
import subprocess
import logging
from argparse import ArgumentParser
import typing
import tempfile
import time
from asyncio_subprocess_examples.runner import runner


def fortran_test_generator() -> typing.Dict[str, str]:
    """
    provides simple code block elements to test compiler feature level
    """

    tests = {
        "minimal": "end",
        "f2008rank15": "integer :: a(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1); print*,rank(a);end",
        "f2008contiguous": "print*,is_contiguous([0,0]); end",
        "f2018errorstop": "character :: a; error stop a; end",
        "f2008version": "use, intrinsic :: iso_fortran_env; print *, compiler_version(); end",
        "f2008block": "block; a=0.; end block; end",
        "f2018randominit": "call random_init(.false., .false.); end",
        "f2018properties": "complex :: z; print *,z%re,z%im,z%kind; end",
    }

    return tests


async def arbiter(compiler: str, Nrun: int, verbose: bool) -> typing.Dict[str, bool]:
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


async def fortran_compiler_ok(compiler: str, name: str, src: str, verbose: bool = False) -> typing.Tuple[str, bool]:
    """ check that Fortran compiler is able to compile a basic program """

    with tempfile.NamedTemporaryFile("w", suffix=".f90", delete=False) as f:
        f.write(src)

    logging.debug("testing {} with source: {}".format(compiler, src))
    cmd = [compiler, f.name]
    # print(' '.join(cmd))
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    # this and delete=False is necessary due to Windows no double-open file limitation
    os.unlink(f.name)

    # print(stdout.decode('utf8'))
    errmsg = stderr.decode("utf8")
    if verbose and errmsg:
        print(stderr.decode("utf8"), file=sys.stderr)

    return name, proc.returncode == 0


def fortran_compiler_ok_sync(compiler: str, name: str, src: str) -> typing.Tuple[str, bool]:
    """ check that Fortran compiler is able to compile a basic program """

    with tempfile.NamedTemporaryFile("w", suffix=".f90", delete=False) as f:
        f.write(src)

    logging.debug("testing {} with source: {}".format(compiler, src))
    cmd = [compiler, f.name]
    ret = subprocess.run(cmd, stderr=subprocess.DEVNULL)

    # this and delete=False is necessary due to Windows no double-open file limitation
    os.unlink(f.name)

    return name, ret.returncode == 0


def main(compiler: str, Nrun: int, verbose: bool):
    if not shutil.which(compiler):
        raise FileNotFoundError(compiler)
    # %% asynch time
    tic = time.monotonic()
    check_results = runner(arbiter, compiler, Nrun, verbose)
    toc = time.monotonic()
    print("{:.3f} seconds to compile asyncio".format(toc - tic))
    # %% synch time
    tic = time.monotonic()
    results = []
    for _ in range(Nrun):  # just to run the tests many times
        for testname, testsrc in fortran_test_generator().items():
            results.append(fortran_compiler_ok_sync(compiler, testname, testsrc))
    results_sync = dict(results)
    toc = time.monotonic()

    print("{:.3f} seconds to compile synchronous".format(toc - tic))

    if sys.version_info >= (3, 6):
        assert results_sync == check_results
    # %% print test outcomes
    if Nrun == 1:
        for k, v in check_results.items():
            if not v:
                print(k, "failed", file=sys.stderr)


if __name__ == "__main__":
    p = ArgumentParser(description="demo of asyncio compiler checks")
    p.add_argument(
        "compiler", help="name of compiler executable, e.g. clang gcc flang gfortran ifort",
    )
    p.add_argument(
        "-n", "--Nrun", help="number of times to run test (benchmarking)", type=int, default=1,
    )
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    main(P.compiler, P.Nrun, P.verbose)
