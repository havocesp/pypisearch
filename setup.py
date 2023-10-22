# -*- coding:utf-8 -*-
"""Pythonic setup.py file."""
from pathlib import Path

import setuptools

_cwf = Path(__file__)
long_description = _cwf.with_name("README.md").read_text(encoding="utf-8")
requirements = _cwf.with_name("requirements.txt").read_text(encoding="utf-8")

setuptools.setup(
    name="pypisearch",
    version='1.3.6',
    author="Havocesp",
    author_email="",
    description="Pip search CLI project finder.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/havocesp/pypisearch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements.splitlines(),
    entry_points={
        "console_scripts":
            [
                "pypisearch=pypisearch.__main__:main",
            ],
    },
)
