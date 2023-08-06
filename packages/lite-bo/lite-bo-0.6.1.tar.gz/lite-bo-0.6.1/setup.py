#!/usr/bin/env python3
import os
from setuptools import setup, find_packages


with open('requirements.txt') as fh:
    requirements = fh.read()
requirements = requirements.split('\n')
requirements = [requirement.strip() for requirement in requirements]


def get_version():
    version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "litebo", "__init__.py")
    for line in open(version_file):
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().replace("'", "").replace('"', '')
            return version
    raise RuntimeError("Unable to find version string in %s" % version_file)


def get_author():
    version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "litebo", "__init__.py")
    for line in open(version_file):
        if line.startswith("__author__"):
            version = line.split("=")[1].strip().replace("'", "").replace('"', '')
            return version
    raise RuntimeError("Unable to find author string in %s" % version_file)


setup(
    name="lite-bo",
    author=get_author(),
    version=get_version(),
    python_requires=">=3.5.2",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    test_suite="nose.collector",
    tests_require=["mock", "nose"]
)
