"""Tests for the string quote checker for class-level docstrings.
"""
from pylint_prosper.func_args_checker import FunctionArgsIndentChecker
import helpers
from pylint import testutils
import astroid

class TestFuncArgIndentChecker(helpers.ProsperCheckerTestCase):
    CHECKER_CLASS = FunctionArgsIndentChecker

    def test_good_function_layout(self):
        """make sure good practice is supported"""
        good_function = '''
def my_good_function(  #@
        arg1,
        arg2,
        optional_arg=None
):
    """docstring"""
    return arg1 + arg2 + optional_arg
'''
        block = astroid.extract_node(good_function)
        with self.assertNoMessages():
            self.checker.visit_functiondef(block)

    def test_bad_function_layout(self):
        """make sure bad format is caught"""
        bad_function = '''
def my_bad_function(arg1,  #@
                    arg2,
                    optional_arg=None
):
    """docstring"""
    return arg1 + arg2 + optional_arg
'''

        block = astroid.extract_node(bad_function)
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='invalid-function-arg-format',
                line=2
            )
        ):
            self.checker.visit_functiondef(block)

    @testutils.set_config(kevlin_func_args=False)
    def test_bad_function_layout_cfg_override(self):
        """make sure bad format is caught"""
        bad_function = '''
def my_bad_function(arg1,  #@
                    arg2,
                    optional_arg=None
):
    """docstring"""
    return arg1 + arg2 + optional_arg
'''

        block = astroid.extract_node(bad_function)

        with self.assertNoMessages():
            self.checker.visit_functiondef(block)

    @testutils.set_config(single_line_args_limit=2)
    def test_single_line_args(self):
        good_oneline_func = '''
def my_oneliner(arg1, arg2):  #@
    """docstring"""
    pass
'''
        block = astroid.extract_node(good_oneline_func)
        with self.assertNoMessages():
            self.checker.visit_functiondef(block)

    @testutils.set_config(single_line_args_limit=2)
    def test_too_many_single_line_args(self):
        """make sure bad one-line format is caught"""
        bad_oneline_func = '''
def my_oneliner(arg1, arg2, arg3):  #@
    """docstring"""
    pass
'''
        block = astroid.extract_node(bad_oneline_func)
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='invalid-oneline-function-format',
                line=2,
                args=2
            )
        ):
            self.checker.visit_functiondef(block)
