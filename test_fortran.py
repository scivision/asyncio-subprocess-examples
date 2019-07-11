#!/usr/bin/env python
import pytest
import os

import compiler_checks as checks

COMPILER = "gfortran"


@pytest.mark.timeout(30)
@pytest.mark.asyncio
@pytest.mark.skipif(os.name == "nt", reason="Pytest-asyncio not setup for Windows yet")
async def test_asyncio():

    result = await checks.fortran_compiler_ok(COMPILER, "minimal", "end")
    assert result[0] == "minimal"
    assert result[1] is True


@pytest.mark.timeout(60)
def test_sync():

    result = checks.fortran_compiler_ok_sync(COMPILER, "minimal", "end")
    assert result[0] == "minimal"
    assert result[1] is True


if __name__ == "__main__":
    pytest.main([__file__])
