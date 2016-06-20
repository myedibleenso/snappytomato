#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools import setup
import re
import os
import sys
# try:
#     from urllib import urlretrieve
# except:
#     from urllib.request import urlretrieve

# use requirements.txt as deps list
with open('requirements.txt') as f:
    required = f.read().splitlines()

# get readme
with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

# get version
with open('snappytomato/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(name='snappytomato',
      version=version,
      keywords=['rotten tomatoes', 'myedibleenso'],
      description="A wrapper for the rottentomatoes API.",
      long_description=readme,
      url='http://github.com/myedibleenso/snappytomato',
      author='myedibleenso',
      author_email='gushahnpowell@gmail.com',
      license='Apache 2.0',
      packages=["snappytomato"],
      install_requires=required,
      classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
      ),
      tests_require=['green', 'coverage'],
      include_package_data=True,
      zip_safe=True)
