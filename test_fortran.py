import asyncio

import compiler_checks as checks

COMPILER = "gfortran"


def test_asyncio():

    result = asyncio.run(checks.arbiter(COMPILER, Nrun=1, verbose=False))
    assert result["minimal"]


def test_sync():

    result = checks.fortran_compiler_ok_sync(COMPILER, "minimal", "end")
    assert result[0] == "minimal"
    assert result[1]
