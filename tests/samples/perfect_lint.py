"""a sample of perfect pylint standards"""
from os import path

HERE = path.abspath(path.dirname(__file__))

def perfect_function(
        pretty_int,
        pretty_optional='butts'
):
    """a perfect sample of a stand-alone function

    Args:
        pretty_int (int): a number
        pretty_optional (str): optional string

    Returns:
        str: concatenated values together

    """
    return 'Hello world: ' + str(pretty_int) + pretty_optional

class PerfectClass:
    """a perfect sample of a class

    Args:
        special_args (int): a number

    """
    def __init__(self, special_args):
        self.special_args = special_args

    def __str__(self):
        return self.special_args

    def do_stuff(self, magic_names):
        """a method that does things

        Args:
            magic_names (:obj:`list): list of names

        Returns:
            str: a special message just for you

        """
        return ', '.join(magic_names) + 'x' + str(self.special_args)

    def dont_do_stuff(self):
        """a method that throws errors

        Raises:
            Exception: go fly a kite

        """
        raise Exception(self.special_args)
