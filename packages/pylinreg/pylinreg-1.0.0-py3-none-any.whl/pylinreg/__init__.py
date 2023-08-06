# -*- coding: utf-8 -*-

"""
PyLinReg
==============================================================================
Linear Regression Model with only Python Standard Library based on
Ordinary Least Squares (OLS) Method
------------------------------------------------------------------------------
Comments are based on PEP 257 with multi-line strings format and a modified
numpy style.
PEP 257: https://www.python.org/dev/peps/pep-0257/
numpy style: https://numpydoc.readthedocs.io/en/latest/format.html
------------------------------------------------------------------------------
MIT License
Copyright (c) 2021 Richárd Ádám Vécsey Dr.
See accompanying file LICENSE.
"""



# constants
__author__ = 'Richárd Ádám Vécsey Dr.'
__copyright__ = "Copyright 2021, PyLinReg"
__credits__ = ['Richárd Ádám Vécsey Dr.']
__license__ = 'MIT'
__version__ = '1.0.0'
__status__ = 'Alpha'



# import section
from importlib import import_module
from ._pylinreg import LinearModel



import_module('pylinreg')
__all__ = ['LinearModel']