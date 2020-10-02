#!/usr/bin/env python3
import sys
import shutil
import asyncio
from argparse import ArgumentParser
import time

import asyncio_subprocess_examples as ase


def main(compiler: str, Nrun: int, verbose: bool):
    if not shutil.which(compiler):
        raise FileNotFoundError(compiler)
    # %% asynch time
    tic = time.monotonic()
    check_results = asyncio.run(ase.arbiter(compiler, Nrun, verbose))
    toc = time.monotonic()
    print(f"{toc - tic:.3f} seconds to compile asyncio")
    # %% synch time
    tic = time.monotonic()
    results = []
    for _ in range(Nrun):  # just to run the tests many times
        for testname, testsrc in ase.fortran_test_generator().items():
            results.append(ase.fortran_compiler_ok_sync(compiler, testname, testsrc))
    results_sync = dict(results)
    toc = time.monotonic()

    print(f"{toc-tic:.3f} seconds to compile synchronous")

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
