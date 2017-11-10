"""PyLint plugin for validating preferred args alignment"""
import tokenize

import pylint.interfaces
import pylint.checkers


MSGS = {
    'E6900': (
        'Invalid indentation, add %s spaces',
        'Invalid function argument alignment',
        'Used when inconsistent tabstops are used in argument list'
    )
}

OPTIONS = (
    'kevlin-func-args',
    dict(
        default=True,
        type='yn',
        metavar='<y or n>',
        help='Enforce newline function args.  A la Kevlin Henny\'s clean code notes'
    )
)
class FunctionArgsIndentChecker(pylint.checkers.BaseTokenChecker):
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

    options = OPTIONS

    def visit_module(self, node):
        """Visit module and check for docstring quote consistency.

        Args:
            node: the module node being visited.

        """
        self._TODO_process(node, 'module')

    # pylint: disable=unused-argument
    def leave_module(self, node):
        """Leave module and check remaining triple quotes.

        Args:
            node: the module node we are leaving.

        """
        pass

        # after we are done checking these, clear out the triple-quote
        # tracking collection so nothing is left over for the next module.
        self._tokenized_triple_quotes = {}


    def _TODO_process(self, node, node_type):
        """Check for docstring quote consistency.

        Args:
            node: the AST node being visited.
            node_type: the type of node being operated on.

        """
        pass
