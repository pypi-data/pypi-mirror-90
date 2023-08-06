#!/usr/bin/env python
"""The package setup script."""
import os
import sys

from setuptools import find_packages, setup


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Jean-Paul van Ravensberg",
    author_email="14926452+DevSecNinja@users.noreply.github.com",
    classifiers=[
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Asynchronous Python wrapper for the Bittrex API.",
    include_package_data=True,
    install_requires=["aiohttp>=3.0.0", "asyncio-throttle>=0.1.1"],
    keywords=[
        "bittrex",
        "bittrex-api",
        "bittrex-v3",
        "cryptocurrency",
        "api",
        "async",
        "client",
    ],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="aiobittrexapi",
    packages=find_packages(include=["aiobittrexapi"]),
    url="https://github.com/DevSecNinja/aiobittrexapi",
    version="1.1.0",
    zip_safe=False,
)
