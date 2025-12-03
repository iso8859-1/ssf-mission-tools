"""Command-line interface for ssf_mission_tools."""
from __future__ import annotations

import argparse
import sys
from dataclasses import asdict
from .config import Config

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ssf-mission-tools")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init= subparsers.add_parser("init", help="Initialize development directory")


    update = subparsers.add_parser("update", help="Update mission files in development directory from the DCS mission")

    build = subparsers.add_parser("build", help="Build the .miz file from the development directory")

    config = subparsers.add_parser("config", help="Configure scripts")
    Config.add_subparser(config)
    return parser

def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else sys.argv[1:]
    parser = create_parser()
    args = parser.parse_args(argv)

    if getattr(args, "version", False):
        from . import __version__
        print(__version__)
        return 0

    if args.command == "config":
        Config.handle_arguments(args)
        return 0

    parser.print_help()
    return 1
