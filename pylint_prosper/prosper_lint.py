"""a wrapper to execute pylint for prosper projects"""
from os import path

from plumbum import local

# TODO: implement prosper_cli parent wrapper
from plumbum.cli import Application as ProsperCLI
#from prosper.common.prosper_cli import cli  #NOT IMPLEMENTED

from _version import __version__

HERE = path.abspath(path.dirname(__file__))

class ProsperLint(ProsperCLI):
    """a pylint wrapper that helps execute pylint checking in CI runs"""
    PROGNAME = 'prosper_lint'
    VERSION = __version__


    def main(self):
        """do stuff here"""
        pass

def run_main():
    """hook for running entry_points"""
    ProsperLint.run()

if __name__ == '__main__':
    run_main()
