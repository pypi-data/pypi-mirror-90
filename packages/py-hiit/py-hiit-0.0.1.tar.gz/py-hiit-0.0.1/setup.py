#!/usr/bin/env python3.8
import io
from setuptools import setup

setup(
    name="py-hiit",
    version="0.0.1",
    description="Functions for creating a HIIT workout.",
    author="Mathew Moon",
    author_email="me@mathewmoon.net",
    url="https://github.com/mathewmoon/py-hiit",
    license="Apache 2.0",
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=["pyhiit"],
    package_dir={"pyhiit": "src"},
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
    ]
)
