#!/usr/bin/env python

#----------------------------------------------------------------------------------------------------------------------------------

# 2+3 compatibility
from __future__ import unicode_literals

# standards
from os import path
import re
import setuptools

#----------------------------------------------------------------------------------------------------------------------------------

with open(path.join(path.dirname(__file__), 'README.md'), 'rb') as file_in:
    long_description = file_in.read().decode('UTF-8')

with open(path.join(path.dirname(__file__), 'klon', 'version.py'), 'rb') as file_in:
    klon_version = re.search(
        r'KLON_VERSION = \'(.+)\'',
        file_in.read().decode('UTF-8'),
    ).group(1)

setuptools.setup(
    name='klon',
    version=klon_version,
    author='Herv\u00e9 Saint-Amand',
    author_email='klon@saintamh.org',
    description='Utilities for building ElementTrees',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/saintamh/klon/',
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
    ],
)

#----------------------------------------------------------------------------------------------------------------------------------
