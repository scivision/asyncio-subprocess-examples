#!/usr/bin/env python3
"""
Errors are raised with .map of ProcessPoolExecutor or ThreadPoolExecutor only when retrieving the result,
as per docs:
https://docs.python.org/3/library/concurrent.futures.html
"""

import concurrent.futures
from typing import Iterator


def main(numbers) -> Iterator[int]:
    """
    The same behavior occurs with ThreadPoolExecutor and ProcessPoolExecutor:
    exception not thrown till iterator is iterated to the exception.
    """

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(timestwo, numbers, timeout=5)

    return results


def timestwo(number: int) -> int:
    err = number * 2

    if err == 8:
        raise RuntimeError(f"The evil value {err} has been reached")

    return err


if __name__ == "__main__":
    numbers = range(1, 5)

    num2 = main(numbers)

    for n in num2:
        if n == 6:
            print("next comes an exception")
