#!/usr/bin/env python
from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ouigo",
    version="1.0.2",
    description="A module which allows you to retrieve data about the cheapest one-way travels of Ouigo "
    "in a date range.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ricardo Alegre",
    author_email="ricardomanuel.alegre@gmail.com",
    url="https://github.com/RicardoAlegreMiranda/ouigo",
    packages=["ouigo"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"]
)
