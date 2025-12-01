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
    init.add_argument("-d", "--directory", type=str, default=".", help="Target directory for initialization")
    init.add_argument("-m", "--mission", type=str, required=True, help="Mission used for initialization")

    update = subparsers.add_parser("update", help="Update mission files in development directory from the DCS mission")

    build = subparsers.add_parser("build", help="Build the .miz file from the development directory")

    config = subparsers.add_parser("config", help="Configure scripts")
    cfg_sub = config.add_subparsers(dest="cfg_cmd", required=False)
    cfg_show = cfg_sub.add_parser("show", help="Show current configuration")
    cfg_save = cfg_sub.add_parser("save", help="Save current configuration to disk")
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
        cfg = Config.load_or_default()
        if getattr(args, "cfg_cmd", None) == "show":
            import json
            data = asdict(cfg)
            data.pop("_app_name", None)
            data.pop("_file_name", None)
            print(json.dumps(data, indent=2, default=str))
            return 0
        if getattr(args, "cfg_cmd", None) == "save":
            cfg.save()
            print(f"Saved config to {cfg._path}")
            return 0

    parser.print_help()
    return 1
