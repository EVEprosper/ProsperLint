"""pylint_prosper module"""
from __future__ import absolute_import

def register(linter):
    """Required method to auto register this checker.

    Notes:
        copied from: https://github.com/edaniszewski/pylint-quotes

    Args:
        linter: Main interface object for Pylint plugins.

    """
    from pylint_prosper.args_checker import ArgsIndentChecker
    linter.register_checker(ArgsIndentChecker(linter))
