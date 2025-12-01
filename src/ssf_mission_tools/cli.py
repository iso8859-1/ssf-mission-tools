"""Command-line interface for ssf_mission_tools."""
from __future__ import annotations

import argparse
import sys

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ssf-mission-tools")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init= subparsers.add_parser("init", help="Initialize development directory")
    init.add_argument("-d", "--directory", type=str, default=".", help="Target directory for initialization")
    init.add_argument("-m", "--mission", type=str, required=True, help="Mission used for initialization")

    update = subparsers.add_parser("update", help="Update mission files in development directory from the DCS mission")

    build = subparsers.add_parser("build", help="Build the .miz file from the development directory")

    config = subparsers.add_parser("config", help="Configure scripts")
    return parser

def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else sys.argv[1:]
    parser = create_parser()
    args = parser.parse_args(argv)

    if getattr(args, "version", False):
        from . import __version__
        print(__version__)
        return 0

    if args.command == "hello":
        print(f"Hello, {args.name}!")
        return 0

    parser.print_help()
    return 1
