"""PyLint docs are garbo, demo pylint testutils
"""

import helpers
from pylint import checkers, testutils
import astroid

class TestPytestUtils(helpers.ProsperCheckerTestCase):
    """demo basic pytest functionality"""
    CHECKER_CLASS = checkers.base.NameChecker
    def test_bad_function_name(self):
        """make sure system yields C0103"""
        bad_function = '''
def BOOTY(butts): #@
    """docstring"""
    print(butts)
'''
        stmt = astroid.extract_node(bad_function)
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='invalid-name',
                node=stmt,
                args=('function', 'BOOTY', '')
            )
        ):
            self.checker.visit_functiondef(stmt)

    def test_good_function_name(self):
        """make sure system doesn't yield C0103"""
        good_function = '''
def booty(butts): #@
    """docstring"""
    print(butts)
'''
        stmt = astroid.extract_node(good_function)
        print(stmt)
        with self.assertNoMessages():
            self.checker.visit_functiondef(stmt)
