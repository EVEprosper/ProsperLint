"""Tests for the string quote checker for class-level docstrings.
"""
from pylint_prosper.args_checker import ArgsIndentChecker
import helpers
from pylint import testutils
import astroid

class TestFuncArgsIndentChecker(helpers.ProsperCheckerTestCase):
    CHECKER_CLASS = ArgsIndentChecker

    def test_good_function(self):
        """make sure good practice is supported"""
        good_function = '''
def my_good_function(  #@
        arg1,
        arg2,
        optional_arg=None
):
    return arg1 + arg2 + optional_arg
'''
        block = astroid.extract_node(good_function)
        with self.assertNoMessages():
            self.checker.visit_functiondef(block)

    def test_good_function_empty(self):
        """make sure good practice is supported"""
        good_function = '''
def my_good_function():  #@
    return arg1 + arg2 + optional_arg
'''
        block = astroid.extract_node(good_function)
        with self.assertNoMessages():
            self.checker.visit_functiondef(block)

    def test_bad_function(self):
        """make sure bad format is caught"""
        bad_function = '''
def my_bad_function(arg1,  #@
                    arg2,
                    optional_arg=None
):
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
    def test_bad_function_override(self):
        """make sure bad format is caught"""
        bad_function = '''
def my_bad_function(arg1,  #@
                    arg2,
                    optional_arg=None
):
    return arg1 + arg2 + optional_arg
'''

        block = astroid.extract_node(bad_function)

        with self.assertNoMessages():
            self.checker.visit_functiondef(block)

    def test_good_oneline_function(self):
        """don't make noise if one-line args are within limit (2)"""
        good_oneline_func = '''
def my_oneliner(arg1, arg2):  #@
    pass
'''
        block = astroid.extract_node(good_oneline_func)
        with self.assertNoMessages():
            self.checker.visit_functiondef(block)

    def test_too_many_oneline_function(self):
        """make sure bad one-line format is caught"""
        bad_oneline_func = '''
def my_oneliner(arg1, arg2, arg3):  #@
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

    @testutils.set_config(single_line_args_limit=3)
    def test_good_oneline_function_custom(self):
        """make sure bad one-line format is caught"""
        bad_oneline_func = '''
def my_oneliner(arg1, arg2, arg3):  #@
    pass
'''
        block = astroid.extract_node(bad_oneline_func)
        with self.assertNoMessages():
            self.checker.visit_functiondef(block)

    @testutils.set_config(single_line_args_limit=3)
    def test_bad_oneline_function_custom(self):
        """make sure bad one-line format is caught"""
        bad_oneline_func = '''
def my_oneliner(arg1, arg2, arg3, arg4):  #@
    pass
'''
        block = astroid.extract_node(bad_oneline_func)
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='invalid-oneline-function-format',
                line=2,
                args=3
            )
        ):
            self.checker.visit_functiondef(block)

class TestMethodArgsIndentChecker(helpers.ProsperCheckerTestCase):
    CHECKER_CLASS = ArgsIndentChecker

    def test_good_method(self):
        """validate methods get the same lint treatment"""
        good_class = '''
class FancyClass:  #@
    """class docstring"""
    def foo(
            self,
            arg1,
            arg2,
            optional_arg=None
    ):
        pass
'''
        block = astroid.extract_node(good_class)
        with self.assertNoMessages():
            self.checker.visit_classdef(block)

    def test_good_method_empty(self):
        """validate methods get the same lint treatment"""
        good_class = '''
class FancyClass:  #@
    """class docstring"""
    def foo():
        pass
'''
        block = astroid.extract_node(good_class)
        with self.assertNoMessages():
            self.checker.visit_classdef(block)

    def test_good_method_many(self):
        """validate all methods are good in class"""
        good_long_class = '''
class FancierClass:  #@
    def foo(
            self,
            arg1,
            arg2,
            optional_arg=None
    ):
        pass

    def bar(
            self,
            arg1,
            arg2,
            optional_arg=None
    ):
        pass
'''
        block = astroid.extract_node(good_long_class)
        with self.assertNoMessages():
            self.checker.visit_classdef(block)

    def test_bad_method(self):
        """validate expected error with invalid args format"""
        bad_class = '''
class BadClass:  #@
    """class docstring"""
    def foo(self,
            arg1,
            arg2,
            optional_arg=None
    ):
        pass
'''
        block = astroid.extract_node(bad_class)
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='invalid-function-arg-format',
                line=4
            )
        ):
            self.checker.visit_classdef(block)

    @testutils.set_config(kevlin_func_args=False)
    def test_bad_method_override(self):
        """validate skip behavior for class args"""
        bad_class = '''
class BadClass:  #@
    """class docstring"""
    def foo(self,
            arg1,
            arg2,
            optional_arg=None
    ):
        pass
'''
        block = astroid.extract_node(bad_class)
        with self.assertNoMessages():
            self.checker.visit_classdef(block)

    def test_good_oneline_method(self):
        """validate one-line method limits (2+1)"""
        good_oneline_class = '''
class OneLineClass:  #@
    def foo(self, arg1, arg2):  # +1 for ``self``
        pass
'''
        block = astroid.extract_node(good_oneline_class)
        with self.assertNoMessages():
            self.checker.visit_classdef(block)

    def test_too_many_oneline_method(self):
        """validate error for too many one-line method args"""
        bad_oneline_class = '''
class OneLineClass:  #@
    def foo(self, arg1, arg2, arg3):  # +1 for ``self``
        pass
'''
        block = astroid.extract_node(bad_oneline_class)
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='invalid-oneline-function-format',
                line=3,
                args=2
            )
        ):
            self.checker.visit_classdef(block)

    @testutils.set_config(single_line_args_limit=3)
    def test_good_oneline_method_custom(self):
        """validate one-line method limits (2+1)"""
        good_oneline_class = '''
class OneLineClass:  #@
    def foo(self, arg1, arg2, arg3):  # +1 for ``self``
        pass
'''
        block = astroid.extract_node(good_oneline_class)
        with self.assertNoMessages():
            self.checker.visit_classdef(block)

    @testutils.set_config(single_line_args_limit=3)
    def test_bad_oneline_method_custom(self):
        """validate error for too many one-line method args"""
        bad_oneline_class = '''
class OneLineClass:  #@
    def foo(self, arg1, arg2, arg3, arg4):  # +1 for ``self``
        pass
'''
        block = astroid.extract_node(bad_oneline_class)
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='invalid-oneline-function-format',
                line=3,
                args=3
            )
        ):
            self.checker.visit_classdef(block)

class TestCallFuncArgsIndentChecker(helpers.ProsperCheckerTestCase):
    CHECKER_CLASS = ArgsIndentChecker

    def test_good_call_func(self):
        """make sure good practice is supported"""
        good_call = '''
result = my_function(
    arg1,
    arg2,
    arg3=None
)
'''
        block = astroid.extract_node(good_call)
        with self.assertNoMessages():
            self.checker.visit_callfunc(block)

    def test_good_call_func_empty(self):
        """make sure good practice is supported"""
        good_call = '''
result = my_function()
'''
        block = astroid.extract_node(good_call)
        with self.assertNoMessages():
            self.checker.visit_callfunc(block)

    def test_bad_call_layout(self):
        """make sure bad format is caught"""
        bad_call = '''
result = my_function(arg1,  #@
                     arg2,
                     optional_arg=None
)
'''

        block = astroid.extract_node(bad_call)
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='invalid-function-arg-format',
                line=2
            )
        ):
            self.checker.visit_callfunc(block)

    @testutils.set_config(kevlin_func_args=False)
    def test_bad_call_layout_override(self):
        """make sure bad format is caught"""
        bad_call = '''
result = my_function(arg1,  #@
                     arg2,
                     optional_arg=None
)
'''

        block = astroid.extract_node(bad_call)
        with self.assertNoMessages():
            self.checker.visit_callfunc(block)
