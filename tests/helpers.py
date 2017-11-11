"""generic test helpers"""
from os import path

import pylint.testutils
import astroid

HERE = path.abspath(path.dirname(__file__))
ROOT = path.join(path.dirname(HERE), 'pylint_prosper')

class ProsperCheckerTestCase(pylint.testutils.CheckerTestCase):
    """instance of checker for pylint tests"""
    pass
