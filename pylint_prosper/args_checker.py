"""PyLint plugin for validating preferred args alignment"""
import tokenize

import pylint.interfaces
import pylint.checkers


MSGS = {
    'E6900': (
        'Argument alignment, move to new line',
        'invalid-function-arg-format',
        'Used when inconsistent tabstops are used in argument list'
    ),
    'E6901': (
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


    def process_tokens(self, tokens):
        """todo"""
        print(tokens)

    def _TODO_process(self, node, node_type):
        """Check for docstring quote consistency.

        Args:
            node: the AST node being visited.
            node_type: the type of node being operated on.

        """
        pass

    def visit_functiondef(self, node):
        """checks for ``def function_name(arg1\n`` pattern

        Args:
            node (:obj:`astroid.node`): function node to grade

        """
        func_lineno = node.fromlineno
        args_lineno = []
        for arg in node.args.args:
            args_lineno.append(arg.lineno)

        ## Check if valid one-line function ##
        one_line_args = len(set(args_lineno)) <= 1
        if one_line_args and len(args_lineno) > self.config.single_line_args_limit:
            self.add_message(
                'invalid-oneline-function-format',
                line=func_lineno,
                args=(self.config.single_line_args_limit)
            )
            return
        elif one_line_args and len(args_lineno) <= self.config.single_line_args_limit:
            return  # valid one-line function

        ## Check if first arg is on same line as function def ##
        if func_lineno == args_lineno[0] and self.config.kevlin_func_args:
            self.add_message(
                'invalid-function-arg-format',
                line=func_lineno
            )
