import asyncio
import os

import asyncio_subprocess_examples as ase

COMPILER = os.environ.get("FC", "gfortran")


def test_asyncio(tmp_path):
    src_files = ase.write_tests(tmp_path)

    result = asyncio.run(ase.arbiter(COMPILER, src_files, Nrun=1, verbose=False))
    assert result["minimal"]


def test_sync(tmp_path):
    for s in ase.write_tests(tmp_path):
        result = ase.fortran_compiler_ok_sync(COMPILER, s)
        assert result[0]
