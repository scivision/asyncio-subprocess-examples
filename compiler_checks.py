#!/usr/bin/env python
import sys
if sys.version_info < (3, 5):
    raise RuntimeError('Python >= 3.5 required')

import os
import asyncio
import subprocess
from argparse import ArgumentParser
from typing import Dict, Tuple
import tempfile
import time


def fortran_test_generator() -> Dict[str, str]:
    """
    this could be read from a file, etc instead for a real implementation
    """

    tests = {
        'minimal': 'end',
        'f2008contiguous': 'print*,is_contiguous([0,0]); end',
        'f2018errorstop': 'character :: a; error stop a; end',
        'f2008version': 'use, intrinsic :: iso_fortran_env; print *, compiler_version(); end',
        'f2008block': 'block; a=0.; end block; end',
        'f2018randominit': 'call random_init(.false., .false.); end',
        'f2018properties': 'complex :: z; print *,z%re,z%im,z%kind; end',
    }

    return tests


async def arbiter(compiler: str, Nrun: int) -> Dict[str, bool]:
    """
    example tests for compilers

    in real use, instead of printing results, we would perhaps return dict
    with compiler capabilites as suitable for main program.
    """

    tests = fortran_test_generator()

    futures = []
    for _ in range(Nrun):  # just to run the tests many times
        for testname, testsrc in tests.items():
            futures.append(fortran_compiler_ok(compiler, testname, testsrc))

    results = await asyncio.gather(*futures)

    return dict(results)


async def fortran_compiler_ok(compiler: str, name: str, src: str) -> Tuple[str, bool]:
    """ check that Fortran compiler is able to compile a basic program """

    with tempfile.NamedTemporaryFile("w", suffix='.f90', delete=False) as f:
        f.write(src)

    # print('testing', compiler, 'with source:', src)
    cmd = [compiler, f.name]
    # print(' '.join(cmd))
    proc = await asyncio.create_subprocess_exec(*cmd,
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    os.unlink(f.name)  # this and delete=False is necessary due to Windows no double-open file limitation

    # print(stdout.decode('utf8'))
    # errmsg = stderr.decode('utf8')
    # if errmsg:
    #     print(stderr.decode('utf8'), file=sys.stderr)

    return name, proc.returncode == 0


def fortran_compiler_ok_sync(compiler: str, name: str, src: str) -> Tuple[str, bool]:
    """ check that Fortran compiler is able to compile a basic program """

    with tempfile.NamedTemporaryFile("w", suffix='.f90', delete=False) as f:
        f.write(src)

    # print('testing', compiler, 'with source:', src)
    cmd = [compiler, f.name]
    ret = subprocess.run(cmd, stderr=subprocess.DEVNULL)

    os.unlink(f.name)  # this and delete=False is necessary due to Windows no double-open file limitation

    return name, ret.returncode == 0


def main(compiler: str, Nrun: int):
    # %% asyncio
    tic = time.monotonic()
    if os.name == 'nt':
        loop = asyncio.ProactorEventLoop()  # type: ignore
    else:
        loop = asyncio.new_event_loop()
        # needed for asyncio-subprocess, when not using Python >= 3.6 asyncio.run()
        asyncio.get_child_watcher().attach_loop(loop)

    check_results = loop.run_until_complete(arbiter(P.compiler, P.Nrun))
    toc = time.monotonic()
    print('{:.3f} seconds to compile asyncio'.format(toc - tic))
# %% sync test
    tic = time.monotonic()
    results = []
    for _ in range(P.Nrun):  # just to run the tests many times
        for testname, testsrc in fortran_test_generator().items():
            results.append(fortran_compiler_ok_sync(P.compiler, testname, testsrc))
    results_sync = dict(results)
    toc = time.monotonic()

    print('{:.3f} seconds to compile synchronous'.format(toc - tic))

    if sys.version_info >= (3, 6):
        assert results_sync == check_results
# %% print test outcomes
    if Nrun == 1:
        print(check_results)


if __name__ == '__main__':
    p = ArgumentParser(description="demo of asyncio compiler checks")
    p.add_argument('compiler', help='name of compiler executable, e.g. clang gcc flang gfortran ifort')
    p.add_argument('-n', '--Nrun', help='number of times to run test (benchmarking)', type=int, default=1)
    P = p.parse_args()

    main(P.compiler, P.Nrun)
