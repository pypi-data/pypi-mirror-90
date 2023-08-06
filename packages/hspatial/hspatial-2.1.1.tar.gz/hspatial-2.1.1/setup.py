#!/usr/bin/env python

import os
import re

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
    "iso8601",
    "htimeseries>=2.0.3,<3",
    "affine",
    "simpletail",
    "gdal>=1.10,<3",
    "django>=1.11,<3",
]

test_requirements = []


def get_version():
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    init_py_path = os.path.join(scriptdir, "hspatial", "__init__.py")
    with open(init_py_path) as f:
        return re.search(r'^__version__ = "(.*?)"$', f.read(), re.MULTILINE).group(1)


setup(
    author="Antonis Christofides",
    author_email="antonis@antonischristofides.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    description="Utilities for spatial integration of time series",
    entry_points={"console_scripts": ["spatialize=hspatial.cli:main"]},
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="hspatial",
    name="hspatial",
    packages=find_packages(include=["hspatial"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/openmeteo/hspatial",
    version=get_version(),
    zip_safe=False,
)
