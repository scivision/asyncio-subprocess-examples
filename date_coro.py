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
        print("{}".format(await t))


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
    runner(coro, P.N)
    print("asyncio.as_completed in {:.3f} seconds".format(time.monotonic() - tic))

    tic = time.monotonic()
    runner(coro_gather, P.N)
    print("asyncio.gather in {:.3f} seconds".format(time.monotonic() - tic))
