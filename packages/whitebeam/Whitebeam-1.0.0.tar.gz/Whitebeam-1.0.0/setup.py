# setup for cython functions
# Whitebeam | Kieran Molloy | Lancaster University 2020

import argparse

from setuptools import setup, Extension, find_packages
from Cython.Distutils import build_ext
import numpy as np
import pathlib

# parser = argparse.ArgumentParser()
# group = parser.add_mutually_exclusive_group(required=True)

# group.add_argument('-c', '--cython', action='store_true')
# group.add_argument('-b', '--build', action='store_true')
# args = parser.parse_args()

NAME = "whitebeam"
VERSION = "0.0.1"
DESCR = "Whitebeam is a framework for creating decision tree functions."
REQUIRES = ["numpy", "cython", "joblib"]

AUTHOR = "Kieran Molloy"
EMAIL = "k.molloy@lancaster.ac.uk"

SRC_DIR = "whitebeam"
PACKAGES = [SRC_DIR]

ext_1 = Extension(SRC_DIR + ".core._whitebeam",
                  sources=[SRC_DIR + "/core/_whitebeam.pyx"],
                  libraries=[],
                  include_dirs=[np.get_include()])

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work

setup(
    name="Whitebeam",
    version="1.0.0",
    description="Whitebeam is a framework for creating decision tree functions.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/K-Molloy/whitebeam",
    author="Kieran Molloy",
    author_email="k.molloy@lancaster.ac.uk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages = find_packages()
    #ext_modules = [ext_1],
    #cmdclass={"build_ext": build_ext},
    #zip_safe=False
)