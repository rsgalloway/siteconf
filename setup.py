#!/usr/bin/env python

from setuptools import setup
from sitecustomize import __version__

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="sitecustomize",
    version=__version__,
    description="Configures sys.path to include hierarchical Python libs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ryan Galloway",
    author_email="ryan@rsgalloway.com",
    py_modules=["sitecustomize"],
    url="http://github.com/rsgalloway/sitecustomize",
    zip_safe=False,
)
