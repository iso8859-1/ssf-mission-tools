from argparse import ArgumentParser
from mimetypes import init
from typing import Any


class Init:
        
    @classmethod
    def add_subparser(cls, parser: ArgumentParser) -> None:
        parser.add_argument("-d", "--directory", type=str, default=".", help="Target directory for initialization")
        parser.add_argument("-m", "--mission", type=str, required=True, help="Mission used for initialization")

    @classmethod
    def handle_arguments(cls, args: Any) -> None:
        pass