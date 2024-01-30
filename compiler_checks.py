#!/usr/bin/env python3
import sys
from pathlib import Path
import shutil
import asyncio
from argparse import ArgumentParser
import time
import tempfile

import asyncio_subprocess_examples as ase


def main(name: str, Nrun: int, verbose: bool):
    if not (exe := shutil.which(name)):
        raise FileNotFoundError(name)

    # %% write test files
    temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)

    src_files = ase.write_tests(Path(temp_dir.name))

    # %% asynch time
    tic = time.monotonic()
    check_results = asyncio.run(ase.arbiter(exe, src_files, Nrun, verbose))
    toc = time.monotonic()
    print(f"{toc - tic:.3f} seconds to compile asyncio")
    # %% synch time
    tic = time.monotonic()
    results = []
    for _ in range(Nrun):  # just to run the tests many times
        for src_file in src_files:
            results.append(ase.fortran_compiler_ok_sync(exe, src_file))
    results_sync = dict(results)
    toc = time.monotonic()

    print(f"{toc - tic:.3f} seconds to compile synchronous")

    temp_dir.cleanup()

    assert results_sync == check_results
    # %% print test outcomes
    if Nrun == 1:
        for k, v in check_results.items():
            if not v:
                print(k, "failed", file=sys.stderr)


if __name__ == "__main__":
    p = ArgumentParser(description="demo of asyncio compiler checks")
    p.add_argument(
        "compiler",
        help="name of compiler executable, e.g. clang gcc flang gfortran ifort",
    )
    p.add_argument(
        "-n",
        "--Nrun",
        help="number of times to run test (benchmarking)",
        type=int,
        default=1,
    )
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    main(P.compiler, P.Nrun, P.verbose)
