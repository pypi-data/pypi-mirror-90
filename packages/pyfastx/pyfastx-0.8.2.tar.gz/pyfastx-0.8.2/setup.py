import os
import sys
import glob
import platform
from setuptools import setup, Extension

link_args = ['-lz', '-lsqlite3']
comp_args = ['-Wno-unused-result']
include_dirs = []
libs = []
lib_dirs = []
define_macros = []

sources = glob.glob('src/*.c')

if os.name == 'nt':
    if '32' in platform.architecture()[0] and sys.version.startswith('3.8'):
        link_args.append('-static-libgcc')
        link_args.append('-static-libstdc++')

    if '64' in platform.architecture()[0]:
        link_args.append('-DMS_WIN64')
        comp_args.append('-DMS_WIN64')
        comp_args.append('-D_FILE_OFFSET_BITS=64')
        comp_args.append('-D_LARGEFILE64_SOURCE=1')
        comp_args.append('-D_LFS64_LARGEFILE=1')

#if sys.platform == 'darwin':
#    link_args.append('-fPIC')
#    comp_args.append('-fPIC')

extension = Extension('pyfastx',
    sources = sources,
    libraries = libs,
    library_dirs = lib_dirs,
    include_dirs = include_dirs,
    extra_compile_args = comp_args,
    extra_link_args = link_args,
    define_macros = define_macros
)

description = (
    "pyfastx is a python module for fast random "
    "access to sequences from plain and gzipped "
    "FASTA/Q file"
)

with open('README.rst') as fh:
    long_description = fh.read()

with open(os.path.join('src', 'version.h')) as fh:
    version = fh.read().split()[2].strip('"')

setup(
    name = 'pyfastx',
    version = version,
    ext_modules = [extension],
    description = description,
    long_description = long_description,
    #long_description_content_type = 'text/x-rst',
    author = 'Lianming Du',
    author_email = 'adullb@qq.com',
    url = 'https://github.com/lmdu/pyfastx',
    license = 'MIT',
    keywords = 'fasta sequence bioinformatics',
    classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "Natural Language :: English",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: C",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Unix",
            "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    entry_points = {
        'console_scripts': ['pyfastx = pyfastxcli:main']
    },
    py_modules = ["pyfastxcli"],
    test_suite = "tests"
)
