#!/usr/bin/env python3
import sys
from pathlib import Path
import shutil
import asyncio
from argparse import ArgumentParser
import time
import tempfile
import os
import subprocess

import asyncio_subprocess_examples as ase


def main(compiler: str, Nrun: int, verbose: bool):
    print(f"Python {sys.version} {sys.platform}")

    if not (exe := shutil.which(compiler)):
        raise FileNotFoundError(compiler)

    try:
        v = subprocess.check_output([exe, "--version"], text=True).split("\n")
        if not (compiler_version := v[0].strip()):
            compiler_version = v[1].strip()
    except subprocess.CalledProcessError:
        compiler_version = ""

    # %% write test files
    temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)

    src_files = ase.write_tests(Path(temp_dir.name))

    # %% asyncio benchmark
    tic = time.monotonic()
    check_results = asyncio.run(ase.arbiter(exe, src_files, Nrun, verbose))
    toc = time.monotonic()
    print(f"{toc - tic:.3f} seconds: asyncio: {compiler} {compiler_version}")

    # %% ThreadPoolExecutor benchmark
    tic = time.monotonic()
    results_thread = ase.fortran_compiler_threadpool(exe, src_files, Nrun)
    toc = time.monotonic()
    print(f"{toc - tic:.3f} seconds: ThreadPoolExecutor: {compiler} {compiler_version}")

    # %% serial benchmark
    tic = time.monotonic()
    results = []
    for _ in range(Nrun):  # just to run the tests many times
        for src_file in src_files:
            results.append(ase.fortran_compiler_ok_sync(exe, src_file))
    results_sync = dict(results)
    toc = time.monotonic()

    print(f"{toc - tic:.3f} seconds: serial: {compiler} {compiler_version}")

    temp_dir.cleanup()

    assert results_sync == results_thread
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
        help="name of compiler executable, e.g. flang gfortran ifx",
        nargs="?",
        default=os.getenv("FC", "gfortran"),
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
