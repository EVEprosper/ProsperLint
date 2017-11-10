"""pylint_prosper module"""
from __future__ import absolute_import

def register(linter):
    """Required method to auto register this checker.

    Notes:
        copied from: https://github.com/edaniszewski/pylint-quotes

    Args:
        linter: Main interface object for Pylint plugins.

    """
    import pylint_prosper.func_args_checker.FunctionArgsIndentChecker as FunctionArgsIndentChecker
    linter.register_checker(FunctionArgsIndentChecker(linter))
