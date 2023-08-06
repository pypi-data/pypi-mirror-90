#!/usr/bin/env python3
''' OctoBase -- The First Building Block For Any Python Project

    Licensed under the Apache License, Version 2.0
    http://www.apache.org/licenses/LICENSE-2.0

    Created and maintained by Octoboxy
    https://octoboxy.com/octobase/
'''

VERSION             = '0.6.1'


booted              = False   # xyzzy -- move somewhere


# Any exceptions we raise should be defined here
from .              import errors


# Massive library of helper functions
from .              import utils


# Fundamental classes from which to build more complex things
from .fundamentals  import Controller, ControllerMixin, Enum, Registry
registry            = Registry()


# Atomic constants
from .              import consts


# A righteous text markup language
from .rightdown     import RightDownData, RightDownOptions


# Our version of unittests
from .fundamentals  import TestCase, TestContext, TestModuleContext, TestRunner
from .              import tests
