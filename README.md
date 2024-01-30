# Python asyncio subprocess Examples

[![ci](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml)

Examples of speedup from Python asyncio-subprocess and ThreadPoolExecutor.
We observe asyncio is faster than ThreadPoolExecutor, which is faster than ProcessPoolExecutor, including on a powerful Linux workstation:

```sh
$ python compiler_checks.py -n 8 gfortran

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.174 seconds: asyncio: GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
0.427 seconds: ThreadPoolExecutor: GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
1.065 seconds: ProcessPoolExecutor: GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
3.630 seconds: serial: GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
```

```sh
$ python compiler_checks.py -n 8 ifx

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.306 seconds: asyncio: ifx (IFX) 2024.0.0 20231017
0.876 seconds: ThreadPoolExecutor: ifx (IFX) 2024.0.0 20231017
1.551 seconds: ProcessPoolExecutor: ifx (IFX) 2024.0.0 20231017
6.870 seconds: serial: ifx (IFX) 2024.0.0 20231017
```

```sh
$ python compiler_checks.py -n 8 nvfortran

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.320 seconds: asyncio: nvfortran 23.11-0
1.056 seconds: ThreadPoolExecutor: nvfortran 23.11-0
1.653 seconds: ProcessPoolExecutor: nvfortran 23.11-0
7.036 seconds: serial: nvfortran 23.11-0
```

macOS Apple Silicon:

```sh
% python compiler_checks.py -n 8

Python 3.11.7 (main, Dec 15 2023, 12:09:56) [Clang 14.0.6 ] darwin

1.282 seconds: asyncio: GNU Fortran (Homebrew GCC 13.2.0) 13.2.0
1.329 seconds: ThreadPoolExecutor: GNU Fortran (Homebrew GCC 13.2.0) 13.2.0
2.330 seconds: ProcessPoolExecutor: GNU Fortran (Homebrew GCC 13.2.0) 13.2.0
5.411 seconds: serial: GNU Fortran (Homebrew GCC 13.2.0) 13.2.0
```

The first example is that of running compiler tests asynchronously, as would possibly be useful for build systems such as Meson.

[compiler_checks.py](./complier_checks.py)

* PC with two physical cores, this script runs at twice the speed of the synchronous (serial) iteration.
* HPC with numerous physical cores, aysncio method runs at four times the speed of serial.

It wasn't immediately clear why the HPC asyncio didn't run much faster than serial for loop.
Was it an issue with the Python script or with some deadlock in the operating system involved in compilation. Hence the reason why we benchmark with an actual compilation task instead of `sleep`.
This time ratio was roughly the same across Fortran compilers.
