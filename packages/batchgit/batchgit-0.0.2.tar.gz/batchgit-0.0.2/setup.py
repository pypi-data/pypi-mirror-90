#!/usr/bin/env python3

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.rst").read_text()

setup(
    name="batchgit",
    version="0.0.2",
    description="Tool to manage multiple git repos",
    long_description=README,
    long_description_content_type="text/x-rst",
    author="Hong Jiang",
    author_email="lazyseq@gmail.com",
    packages=find_packages(exclude=["tests*"]),
    install_requires=["gitpython", "pyyaml"],
    entry_points={
        "console_scripts": [
            "batchgit = batchgit.cli:main",
        ],
    },
)
