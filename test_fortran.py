import asyncio

import asyncio_subprocess_examples as ase

COMPILER = "gfortran"


def test_asyncio():

    result = asyncio.run(ase.arbiter(COMPILER, Nrun=1, verbose=False))
    assert result["minimal"]


def test_sync():

    result = ase.fortran_compiler_ok_sync(COMPILER, "minimal", "end")
    assert result[0] == "minimal"
    assert result[1]
