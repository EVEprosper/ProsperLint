"""PyLint plugin for validating preferred args alignment"""
import tokenize

import pylint.interfaces
import pylint.checkers


MSGS = {
    'E7700': (
        'Argument alignment, move to new line',
        'invalid-function-arg-format',
        'Used when inconsistent tabstops are used in argument list'
    ),
    'E7701': (
        'Too many args for one-line.  More than %s args',
        'invalid-oneline-function-format',
        'Used when one-liner function call is too complex'
    )
}

class ArgsIndentChecker(pylint.checkers.BaseTokenChecker):
    """PyLint checker for enforcing Kevlin Henny's function arg preference

    ..code-block:: python

        # technically valid PEP8 but ugly
        def my_bad_func(arg1
                        arg2,
                        optional_arg=None):
        '''docstring for function'''
            ...

        # preferred format
        def my_good_func(
                arg1,
                arg2,
                optional_arg=None
        ):
            '''docstring for function'''
            ...


    Notes:
        based off https://github.com/edaniszewski/pylint-quotes

    """
    __implements__ = (
        pylint.interfaces.ITokenChecker,
        pylint.interfaces.IAstroidChecker,
    )

    name = 'function_args'

    msgs = MSGS

    options = (
        (
            'kevlin-func-args',
            dict(
                default=True,
                type='yn',
                metavar='<y or n>',
                help='Enforce newline function args.  A la Kevlin Henny\'s clean code notes'
            )
        ),
        (
            'single-line-args-limit',
            dict(
                default=2,
                type='int',
                metavar='<int>',
                help='number of args allowed to be on a single line'

            )
        )
    )


    def process_tokens(self, tokens):  # pragma: no cover
        """Not used?  Passing"""
        pass

    def visit_callfunc(self, node):
        """checks for ``results = do_something(arg1\n`` pattern in call functions"""
        call_lineno = node.value.lineno
        args = node.value.args
        self._check_node_args_style(call_lineno, args)

    def visit_classdef(self, node):
        """checks for ``def function_name(arg1\n`` pattern in methods

        Args:
            node (:obj:`astroid.node`): function node to grade

        """
        for function_node in node.locals.values():
            method_node = function_node[0]
            method_lineno = method_node.fromlineno
            method_args = method_node.args.args
            self._check_node_args_style(
                method_lineno,
                method_args,
                oneline_limit_adjust=1
            )

    def visit_functiondef(self, node):
        """checks for ``def function_name(arg1\n`` pattern

        Args:
            node (:obj:`astroid.node`): function node to grade

        """
        func_lineno = node.fromlineno
        args = node.args.args
        self._check_node_args_style(func_lineno, args)

    def _check_node_args_style(
            self,
            func_lineno,
            args_list,
            oneline_limit_adjust=0
    ):
        """do the actual work of finding bad args lines

        Args:
            func_lineno (int): starting line number
            args_list (:obj:`list`): node.args values of function args
            oneline_limit_adjust (int, optional): +/- adjustments of args limit for special cases

        """
        ## Check if valid one-line call ##
        oneline_limit = self.config.single_line_args_limit + oneline_limit_adjust
        is_oneline = len(set([arg.lineno for arg in args_list])) <= 1  # all args on same line?
        if is_oneline and len(args_list) > oneline_limit:
            self.add_message(
                'invalid-oneline-function-format',
                line=func_lineno,
                args=(self.config.single_line_args_limit)
            )
            return
        if is_oneline and len(args_list) <= oneline_limit:
            return  # valid one-line function

        ## Check if first arg is on same line as function def ##
        if func_lineno == args_list[0].lineno and self.config.kevlin_func_args:
            self.add_message(
                'invalid-function-arg-format',
                line=func_lineno
            )
