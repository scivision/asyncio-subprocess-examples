# Python asyncio subprocess Examples

[![ci](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml)

Examples of parallel compiler speedup from Python
[asyncio-subprocess](https://docs.python.org/3/library/asyncio-subprocess.html),
[ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor),
and
[ProcessPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor).
We observe asyncio is faster than ThreadPoolExecutor, which is faster than ProcessPoolExecutor.

These results may be useful for
[Meson maintainers](https://github.com/mesonbuild/meson/issues/3635)
and CMake maintainers to consider making some
[CMake internals parallelized](https://gitlab.kitware.com/cmake/cmake/-/issues/25595).

The benchmarks below run compilers many times as a real-world example of performance improvements via different techniques in Python.
These same relative speedups may hold similarly true in other coding languages.

## Benchmarks

The benchmark is of compiling ~ 15 small test Fortran source files as defined in `fortran_test_generator()` "Nrun" times.
For example, the benchmarks below use the respective compilers 8 * 15 = 120 times to help stabilize results. 
The test Fortran source files are written once in a tempfile.TemporaryDirectory outside the benchmark loop.

Linux workstation:

Gfortran:

```sh
$ python compiler_checks.py -n 8 gfortran

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.174 seconds: asyncio: GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
0.427 seconds: ThreadPoolExecutor: GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
1.065 seconds: ProcessPoolExecutor: GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
3.630 seconds: serial: GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
```

Intel oneAPI

```sh
$ python compiler_checks.py -n 8 ifx

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.306 seconds: asyncio: ifx (IFX) 2024.0.0 20231017
0.876 seconds: ThreadPoolExecutor: ifx (IFX) 2024.0.0 20231017
1.551 seconds: ProcessPoolExecutor: ifx (IFX) 2024.0.0 20231017
6.870 seconds: serial: ifx (IFX) 2024.0.0 20231017
```

NVHPC

```sh
$ python compiler_checks.py -n 8 nvfortran

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.320 seconds: asyncio: nvfortran 23.11-0
1.056 seconds: ThreadPoolExecutor: nvfortran 23.11-0
1.653 seconds: ProcessPoolExecutor: nvfortran 23.11-0
7.036 seconds: serial: nvfortran 23.11-0
```

AMD AOCC

```sh
$ python compiler_checks.py -n 8 flang

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.284 seconds: asyncio: flang AMD clang version 16.0.3 (CLANG: AOCC_4.1.0-Build#270 2023_07_10)
1.009 seconds: ThreadPoolExecutor: flang AMD clang version 16.0.3 (CLANG: AOCC_4.1.0-Build#270 2023_07_10)
1.638 seconds: ProcessPoolExecutor: flang AMD clang version 16.0.3 (CLANG: AOCC_4.1.0-Build#270 2023_07_10)
8.014 seconds: serial: flang AMD clang version 16.0.3 (CLANG: AOCC_4.1.0-Build#270 2023_07_10)
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
