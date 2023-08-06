#!/usr/bin/env python
# -*- coding: utf-8 -*-
# based on template: https://github.com/kennethreitz/setup.py
import io
import os
import sys
import typing
from shutil import rmtree

from setuptools import Command
from setuptools import find_packages
from setuptools import setup

import versioneer

# Package meta-data.
NAME = "srtools"
DESCRIPTION = "Serbian language Cyrillic ↔ Latin transliteration tools"
URL = "https://gitlab.com/andrejr/srtools"
EMAIL = "r.andrej@gmail.com"
AUTHOR = "Andrej Radović"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = None

# What packages are required for this module to be executed?
REQUIRED: typing.List[str] = []

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# # Load the package's __version__.py module as a dictionary.
# about:typing.Dict[str, typing.List[str]] = {}
# if not VERSION:
#     with open(os.path.join(here, NAME, "__version__.py")) as f:
#         exec(f.read(), about)
# else:
#     about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []  # type:typing.List[str]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(
            "{} setup.py sdist bdist_wheel --universal".format(sys.executable)
        )

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{}".format(versioneer.get_version()))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/x-rst; charset=UTF-8",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests", "benchmarks")),
    install_requires=REQUIRED,
    include_package_data=True,
    license="GPLv3+",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: Serbian",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        "Topic :: Software Development :: Localization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
    scripts=["bin/srts"]
    # $ setup.py publish support.
    # cmdclass={"upload": UploadCommand},
)
