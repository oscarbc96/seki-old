#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/kennethreitz/setup.py

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "seki"
DESCRIPTION = "Automated security tools made easy."
URL = "https://github.com/oscarbc96/seki"
EMAIL = "oscarbc1996@gmail.com"
AUTHOR = "Oscar Blanco Castan"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = None

# What packages are required for this module to be executed?
REQUIRES = [
    "requests",
    "pybitbucket",
    "GitPython"
]

# What packages are optional?
DEV_REQUIRES = [
    "flake8"
]

# The rest you shouldn"t have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if "README.md" is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package"s __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=["seki"],
    entry_points={
        "console_scripts": ["seki=seki.seki:main"],
    },
    install_requires=REQUIRES,
    extras_require={
        "dev": DEV_REQUIRES,
    },
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ]
)