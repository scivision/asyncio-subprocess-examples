# Python asyncio subprocess Examples

[![ci](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/asyncio-subprocess-examples/actions/workflows/ci.yml)

Examples of speedup from Python asyncio-subprocess and ThreadPoolExecutor.
We observe asyncio is faster than ThreadPoolExecutor, including on a powerful Linux workstation:

```sh
$ python compiler_checks.py -n 8 gfortran

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.175 seconds: asyncio: gfortran GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
0.432 seconds: ThreadPoolExecutor: gfortran GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
3.637 seconds: serial: gfortran GNU Fortran (GCC) 11.4.1 20231218 (Red Hat 11.4.1-3)
```

```sh
python compiler_checks.py -n 8 ifx

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.307 seconds: asyncio: ifx ifx (IFX) 2024.0.0 20231017
0.878 seconds: ThreadPoolExecutor: ifx ifx (IFX) 2024.0.0 20231017
7.086 seconds: serial: ifx ifx (IFX) 2024.0.0 20231017
```

```sh
$ python compiler_checks.py -n 8 nvfortran

Python 3.11.7 (main, Dec 15 2023, 18:12:31) [GCC 11.2.0] linux

0.318 seconds: asyncio: nvfortran nvfortran 23.11-0 64-bit
1.040 seconds: ThreadPoolExecutor: nvfortran nvfortran 23.11-0
7.071 seconds: serial: nvfortran nvfortran 23.11-0
```

macOS Apple Silicon:

```sh
% python compiler_checks.py -n 8

Python 3.11.7 (main, Dec 15 2023, 12:09:56) [Clang 14.0.6 ] darwin

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
