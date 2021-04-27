#!/usr/bin/env python3
"""
in general, the times printed may be out of order due to concurrent operations
"""

import asyncio
import sys
import time
from argparse import ArgumentParser

import asyncio_subprocess_examples  # noqa: F401


async def coro_gather(N: int):
    """
    this also works, but waits till all done to give output
    """
    futures = [get_date() for _ in range(N)]
    times = await asyncio.gather(*futures)
    print("\n".join(times))


async def coro(N: int):
    futures = [get_date() for _ in range(N)]
    for t in asyncio.as_completed(futures):
        print(f"{await t}")


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
    p.add_argument("N", help="number of times to print", nargs="?", type=int, default=15)
    P = p.parse_args()

    tic = time.monotonic()
    asyncio.run(coro(P.N))
    toc = time.monotonic()
    print(f"asyncio.as_completed in {toc - tic:.3f} seconds")

    tic = time.monotonic()
    asyncio.run(coro_gather(P.N))
    toc = time.monotonic()
    print(f"asyncio.gather in {toc - tic:.3f} seconds")
