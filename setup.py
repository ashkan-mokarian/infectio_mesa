#!/usr/bin/env python
from setuptools import find_packages, setup

requires = ["mesa"]

setup(
    name="infectio_mesa",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requires,
)
