# Python asyncio subprocess Examples

[![ci](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml)

Examples of speedup from Python asyncio-subprocess and ThreadPoolExecutor.
We observe asyncio is faster than ThreadPoolExecutor, including on a powerful Linux workstation:

```sh
$ python compiler_checks.py -n 16 gfortran

0.320 seconds: asyncio: gfortran
0.808 seconds: ThreadPoolExecutor: gfortran
6.813 seconds: serial: gfortran
```

```sh
$ python compiler_checks.py -n 16 ifx

0.532 seconds: asyncio: ifx
1.760 seconds: ThreadPoolExecutor: ifx
14.147 seconds: serial: ifx
```

macOS Apple Silicon:

```sh
% python compiler_checks.py -n 8

1.348 seconds: asyncio: gfortran GNU Fortran (Homebrew GCC 13.2.0) 13.2.0
1.395 seconds: ThreadPoolExecutor: gfortran GNU Fortran (Homebrew GCC 13.2.0) 13.2.0
5.452 seconds: serial: gfortran GNU Fortran (Homebrew GCC 13.2.0) 13.2.0
```

The first example is that of running compiler tests asynchronously, as would possibly be useful for build systems such as Meson.

[compiler_checks.py](./complier_checks.py)

* PC with two physical cores, this script runs at twice the speed of the synchronous (serial) iteration.
* HPC with numerous physical cores, aysncio method runs at four times the speed of serial.

It wasn't immediately clear why the HPC asyncio didn't run much faster than serial for loop.
Was it an issue with the Python script or with some deadlock in the operating system involved in compilation. Hence the reason why we benchmark with an actual compilation task instead of `sleep`.
This time ratio was roughly the same across Fortran compilers.
