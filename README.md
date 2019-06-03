[![Build Status](https://travis-ci.com/scivision/asyncio-subprocess-examples.svg?branch=master)](https://travis-ci.com/scivision/asyncio-subprocess-examples)

# Python asyncio subprocess Examples

Examples of speedup from Python asyncio-subprocess.

The first example is that of running compiler tests asynchronously, as would possibly be useful for build systems such as Meson.

[compiler_checks.py](./complier_checks.py)

* PC with two physical cores, this script runs at twice the speed of the synchronous (serial) iteration.
* HPC with numerous physical cores, aysncio method runs at four times the speed of serial.

It wasn't immediately clear why the HPC asyncio didn't run much faster than serial for loop.
Was it an issue with the Python script or with some deadlock in the operating system involved in compilation. Hence the reason why we benchmark with an actual compilation task instead of `sleep`.
This time ratio was roughly the same across Fortran compilers.
