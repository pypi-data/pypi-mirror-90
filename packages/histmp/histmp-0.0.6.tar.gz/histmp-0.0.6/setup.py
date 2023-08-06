# BSD 3-Clause License
#
# Copyright (c) 2019, Doug Davis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import codecs
import glob
import os
import re
import pathlib
import subprocess
import sys
import tempfile

import setuptools
from setuptools import setup
from setuptools.extension import Extension

import pybind11
import numpy

def has_flag(compiler, flag):
    """check if compiler has compatibility with the flag"""
    with tempfile.NamedTemporaryFile("w", suffix=".cpp") as f:
        f.write("int main (int argc, char** argv) { return 0; }")
        try:
            compiler.compile([f.name], extra_postargs=[flag])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def get_cpp_std_flag():
    compiler = setuptools.distutils.ccompiler.new_compiler()
    setuptools.distutils.sysconfig.customize_compiler(compiler)
    if has_flag(compiler, "-std=c++14"):
        return "-std=c++14"
    elif has_flag(compiler, "-std=c++11"):
        return "-std=c++11"
    else:
        raise RuntimeError("C++11 (or later) compatible compiler required")


def conda_darwin_flags(flavor="inc"):
    if os.getenv("CONDA_PREFIX"):
        pref = os.getenv("CONDA_PREFIX")
    elif os.getenv("PREFIX"):
        pref = os.getenv("PREFIX")
    else:
        return []
    if flavor == "inc":
        return [f"-I{pref}/include"]
    elif flavor == "lib":
        return [f"-Wl,-rpath,{pref}/lib", f"-L{pref}/lib"]
    else:
        return []


def get_compile_flags(is_cpp=False):
    """get the compile flags"""
    if is_cpp:
        cpp_std = get_cpp_std_flag()
    cflags = ["-Wall", "-Wextra"]
    debug_env = os.getenv("HISTMP_DEBUG")
    if debug_env is None:
        cflags += ["-g0"]
    else:
        cflags += ["-g"]
    if sys.platform.startswith("darwin"):
        if is_cpp:
            cflags += ["-fvisibility=hidden", "-stdlib=libc++", cpp_std]
        cflags += ["-Xpreprocessor", "-fopenmp"]
        cflags += conda_darwin_flags("inc")
    else:
        if is_cpp:
            cflags += ["-fvisibility=hidden", cpp_std]
        cflags += ["-fopenmp"]
    return cflags


def get_link_flags(is_cpp=False):
    lflags = []
    if sys.platform.startswith("darwin"):
        lflags += conda_darwin_flags("lib")
        lflags += ["-lomp"]
    else:
        lflags += ["-lgomp"]
    return lflags


def has_openmp():
    test_code = """
    #include <omp.h>
    #include <stdio.h>
    int main() {
      #pragma omp parallel
      printf("nthreads=%d\\n", omp_get_num_threads());
      return 0;
    }
    """
    has_omp = False
    compiler = setuptools.distutils.ccompiler.new_compiler()
    setuptools.distutils.sysconfig.customize_compiler(compiler)
    cflags = get_compile_flags()
    lflags = get_link_flags()
    tmp_dir = tempfile.mkdtemp()
    start_dir = pathlib.PosixPath.cwd()
    try:
        os.chdir(tmp_dir)
        with open("test_openmp.c", "w") as f:
            f.write(test_code)
        os.mkdir("obj")
        compiler.compile(["test_openmp.c"], output_dir="obj", extra_postargs=cflags)
        objs = glob.glob(os.path.join("obj", "*{}".format(compiler.obj_extension)))
        compiler.link_executable(objs, "test_openmp", extra_postargs=lflags)
        output = subprocess.check_output("./test_openmp")
        output = output.decode(sys.stdout.encoding or "utf-8").splitlines()
        if "nthreads=" in output[0]:
            nthreads = int(output[0].strip().split("=")[1])
            if len(output) == nthreads:
                has_omp = True
            else:
                has_omp = False
        else:
            has_omp = False
    except (
        setuptools.distutils.errors.CompileError,
        setuptools.distutils.errors.LinkError,
    ):
        has_omp = False
    finally:
        os.chdir(start_dir)

    return has_omp


def get_extensions():
    c_cflags = get_compile_flags()
    c_lflags = get_link_flags()
    cpp_cflags = get_compile_flags(is_cpp=True)
    cpp_lflags = get_link_flags(is_cpp=True)
    extenmods = [
        Extension(
            "histmp._CPP",
            [os.path.join("src", "_backend.cpp")],
            language="c++",
            include_dirs=[numpy.get_include()],
            extra_compile_args=cpp_cflags,
            extra_link_args=cpp_lflags,
        ),
        Extension(
            "histmp._CPP_PB",
            [os.path.join("src", "_backend_pb.cpp")],
            language="c++",
            include_dirs=[pybind11.get_include()],
            extra_compile_args=cpp_cflags,
            extra_link_args=cpp_lflags,
        ),
        Extension(
            "histmp._C",
            [os.path.join("src", "_backend.c")],
            language="c",
            include_dirs=[numpy.get_include()],
            extra_compile_args=c_cflags,
            extra_link_args=c_lflags,
        ),
    ]
    return extenmods


if not has_openmp():
    sys.exit(
        "\n"
        "****************************************************\n"
        "* OpenMP not available, aborting installation.     *\n"
        "* On macOS you can install `libomp` with Homebrew. *\n"
        "* On Linux check your GCC installation.            *\n"
        "****************************************************"
    )


setup(
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    ext_modules=get_extensions(),
    zip_safe=False,
)
