#!/usr/bin/env python
"""
in general, the times printed may be out of order due to concurrent operations

Python >= 3.5
"""
import asyncio
import sys
import time
from argparse import ArgumentParser
from asyncio_subprocess_examples.runner import runner


async def coro(N: int):
    return await asyncio.gather(*[get_date() for _ in range(N)])


async def get_date() -> str:
    code = "import datetime; print(datetime.datetime.now())"

    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-c", code, stdout=asyncio.subprocess.PIPE
    )

    # Read one line of output.
    data = await proc.stdout.readline()
    line = data.decode("ascii").rstrip()

    # Wait for the subprocess exit (ur use proc.communicate() if all lines desired)
    await proc.wait()
    return line


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument(
        "N", help="number of times to print", nargs="?", type=int, default=15
    )
    P = p.parse_args()

    tic = time.monotonic()
    result = runner(coro, P.N)
    print("{}\n in {:.3f} seconds".format("\n".join(result), time.monotonic() - tic))
