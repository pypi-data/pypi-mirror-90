#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import sys
from setuptools import setup, find_packages, Extension
from distutils.command.build_ext import build_ext

__version__ = "2.6.4"

cls_txt = """
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering
Operating System :: Unix
Operating System :: POSIX :: Linux
Operating System :: MacOS :: MacOS X
Natural Language :: English
"""

short_desc = "plugin for arfx to read pcmseq files"

class BuildExt(build_ext):
    def build_extensions(self):
        import numpy
        compiler_settings = {"include_dirs": []}
        compiler_settings["include_dirs"].insert(0, "include")
        compiler_settings["include_dirs"].append(numpy.get_include())
        c_opts = []
        for ext in self.extensions:
            for k, v in compiler_settings.items():
                setattr(ext, k, v)
            ext.extra_compile_args.extend(c_opts)
        build_ext.build_extensions(self)

setup(
    name="arfx-plugin-pcmseqio",
    version=__version__,
    description=short_desc,
    classifiers=[x for x in cls_txt.split("\n") if x],
    author="Dan Meliza",
    author_email="dan@meliza.org",
    maintainer="Dan Meliza",
    maintainer_email="dan@meliza.org",
    url="https://github.com/melizalab/arfx-plugin-pcmseqio",

    packages=find_packages(exclude=["*test*"]),
    ext_modules=[Extension("src.pcmseqio",
                           sources=["src/pcmseqio.c", "src/pcmseq.c"]),],

    cmdclass={"build_ext": BuildExt},

    entry_points={"arfx.io": [".pcm_seq2 = src.pcmseqio:pseqfile",
                              ".pcm_seq = src.pcmseqio:pseqfile",
                              ".pcmseq2 = src.pcmseqio:pseqfile",
                              ],
                  },

    install_requires=["numpy"],
    test_suite="tests"
)
# Variables:
# End:
