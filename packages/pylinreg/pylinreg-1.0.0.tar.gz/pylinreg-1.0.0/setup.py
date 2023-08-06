# -*- coding: utf-8 -*-
"""
PyLinReg
==============================================================================
Linear Regression Model with only Python Standard Library based on
Ordinary Least Squares (OLS) Method
------------------------------------------------------------------------------
MIT License
Copyright (c) 2021 Richárd Ádám Vécsey Dr.
See accompanying file LICENSE.
"""



# import section
import os.path
from setuptools import setup

# README
actual_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(actual_directory, 'README.md')) as fh:
    long_description = fh.read()

# setup()
setup(
    name='pylinreg',
    version='1.0.0',
    description='Linear Regression Model with only Python Standard Library based on Ordinary Least Squares (OLS) Method',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/richardvecsey/PyLinReg',
    author='Real Python',
    license='MIT',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 'Operating System :: OS Independent',],
    packages=['pylinreg'],
    include_package_data=True,
    python_requires='>=3.6',)