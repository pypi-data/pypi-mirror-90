#!/usr/bin/env python
# Copyright (c) 2002-2005 ActiveState Software Ltd.

"""preprocess: a multi-language preprocessor

There are millions of templating systems out there (most of them
developed for the web). This isn't one of those, though it does share
some basics: a markup syntax for templates that are processed to give
resultant text output.  The main difference with `preprocess.py` is
that its syntax is hidden in comments (whatever the syntax for comments
maybe in the target filetype) so that the file can still have valid
syntax. A comparison with the C preprocessor is more apt.

`preprocess.py` is targetted at build systems that deal with many
types of files. Languages for which it works include: C++, Python,
Perl, Tcl, XML, JavaScript, CSS, IDL, TeX, Fortran, PHP, Java, Shell
scripts (Bash, CSH, etc.) and C#. Preprocess is usable both as a
command line app and as a Python module.
"""

import os
import sys
import distutils
import re
from setuptools import setup

version = '.'.join(re.findall('__version_info__ = \((\d+), (\d+), (\d+)\)',
                              open('lib/preprocess.py', 'r').read())[0])

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Operating System :: OS Independent
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Text Processing :: Filters
"""

if sys.version_info < (2, 3):
    # Distutils before Python 2.3 doesn't accept classifiers.
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key("classifiers"):
            del kwargs["classifiers"]
        _setup(**kwargs)

doclines = __doc__.split("\n")

setup(
    name="preprocess",
    version=version,
    author="Trent Mick",
    author_email="trentm@gmail.com",
    maintainer="Kristian Gregorius Hustad",
    maintainer_email="krihus@ifi.uio.no",
    url="http://github.com/doconce/preprocess/",
    license="http://www.opensource.org/licenses/mit-license.php",
    platforms=["any"],
    py_modules=["preprocess"],
    package_dir={"": "lib"},
    entry_points={'console_scripts': ['preprocess = preprocess:main']},
    install_requires=['future'],
    description=doclines[0],
    classifiers=filter(None, classifiers.split("\n")),
    long_description="\n".join(doclines[2:]),
)
