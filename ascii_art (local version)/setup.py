#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name = "ascii_art",
    version = "3.0",
    description = "Make ascii art using python",
    python_requires=">=3.5",
    keywords = "ascii art image fun memes",
    install_requires = [
        "colorama==0.4.4",
        "Pillow==8.0.1",
    ],
    packages = find_packages(exclude=["Media"]),
    scripts=["bin/ascii_art"],
)
