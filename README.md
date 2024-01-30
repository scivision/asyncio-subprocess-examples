# Python asyncio subprocess Examples

[![ci](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml)

Examples of parallel compiler speedup from Python asyncio-subprocess, ThreadPoolExecutor, and ProcessPoolExecutor.
We observe asyncio is faster than ThreadPoolExecutor, which is faster than ProcessPoolExecutor.

These results may be useful for
[Meson maintainers](https://github.com/mesonbuild/meson/issues/3635)
and CMake maintainers to consider making some
[CMake internals parallelized](https://gitlab.kitware.com/cmake/cmake/-/issues/25595).

## Benchmarks

Linux workstation:

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
