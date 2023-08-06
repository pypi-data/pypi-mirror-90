#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import setuptools
from setuptools.command.build_py import build_py

NAME = "gaget"
DESCRIPTION = "Download customer data"
URL = "https://github.com/ConductorTechnologies/gaget"
EMAIL = "julian@conductortech.com"
AUTHOR = "Julian Mann"
REQUIRES_PYTHON = "~=3.7"
REQUIRED = [
    "boto3>=1.14.0,<2.0.0",
    "google-cloud-datastore>=1.13.0,<2.0.0",
    "google-cloud-storage>=1.29.0,<2.0.0"
]
HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()


class BuildCommand(build_py):
    def run(self):
        build_py.run(self)
        if not self.dry_run:
            target_dir = os.path.join(self.build_lib, NAME)
            with open(os.path.join(target_dir, "VERSION"), "w") as f:
                f.write(VERSION)

setuptools.setup(
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python"
    ],
    cmdclass={"build_py": BuildCommand},
    description=DESCRIPTION,
    entry_points={"console_scripts": ["gaget=gaget.gaget:main"]},
    include_package_data=True,
    install_requires=REQUIRED,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    name=NAME,
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=REQUIRES_PYTHON,
    url=URL,
    version=VERSION,
    zip_safe=False
)
