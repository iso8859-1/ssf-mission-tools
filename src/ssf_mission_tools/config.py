"""Configuration helper for ssf_mission_tools.

Implements a Config dataclass with defaults, load/save to a JSON file
in the user's config directory (per-platform).
"""
from __future__ import annotations

from argparse import ArgumentParser
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from ssf_mission_tools.common import expand_path

def get_dcs_saved_games_dir() -> Path:
    standard_path = os.path.join(os.path.expanduser("~"), "Saved Games", "DCS")
    open_beta_path = os.path.join(os.path.expanduser("~"), "Saved Games", "DCS.openbeta")    

    if os.path.exists(standard_path):
        return standard_path
    elif os.path.exists(open_beta_path):
        return open_beta_path
    
def get_dcs_saved_games_missions_dir():
    saved_games_dir = get_dcs_saved_games_dir()
    saved_games_missions_dir = os.path.join(saved_games_dir, "Missions")
    os.makedirs(saved_games_missions_dir, exist_ok=True)
    return Path(saved_games_missions_dir)

def _user_config_dir(app_name: str) -> Path:
    # Follow XDG on *nix, use %APPDATA% on Windows, fallback to home
    if os.name == "nt":
        base = os.getenv("APPDATA") or Path.home() / "AppData" / "Roaming"
    else:
        base = os.getenv("XDG_CONFIG_HOME") or Path.home() / ".config"
    return Path(base) / app_name

@dataclass
class Config:
    #extra: Dict[str, Any] = field(default_factory=dict)
    mission_dir: str = field(default_factory=lambda: get_dcs_saved_games_missions_dir().as_posix())
    dcs_path: str = "C:/Program Files/Eagle Dynamics/DCS World"
    
    _app_name: str = field(init=False, repr=False, default="ssf-mission-tools")
    _file_name: str = field(init=False, repr=False, default="config.json")

    @property
    def _path(self) -> Path:
        return _user_config_dir(self._app_name) / "ssf-mission-tools.config.json"

    def load(self) -> None:
        p = self._path
        if not p.exists():
            return
        try:
            with p.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            return
        # Merge keys from JSON onto this dataclass
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                self.extra[k] = v

    def save(self) -> None:
        p = self._path
        # ensure parent directory exists
        p.parent.mkdir(parents=True, exist_ok=True)
        data = asdict(self)
        # remove internal fields
        data.pop("_app_name", None)
        data.pop("_file_name", None)
        # write JSON
        with p.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)

    @classmethod
    def load_or_default(cls) -> "Config":
        cfg = cls()
        cfg.load()
        return cfg
    
    @classmethod
    def add_subparser(cls, parser: ArgumentParser) -> None:
        cfg_sub = parser.add_subparsers(dest="cfg_cmd", required=False)
        cfg_show = cfg_sub.add_parser("show", help="Show current configuration")
        cfg_save = cfg_sub.add_parser("save", help="Change configuration file ")
        cfg_delete = cfg_sub.add_parser("delete", help="Delete the configuration file")
        cfg_save.add_argument("--mission-dir", type=str, help="Change mission directory of DCS")
        cfg_save.add_argument("--dcs-path", type=str, help="Change DCS installation path")

    @classmethod
    def handle_arguments(cls, args: Any) -> None:
        cfg = Config.load_or_default()
        if getattr(args, "cfg_cmd", None) == "show":
            import json
            data = asdict(cfg)
            data.pop("_app_name", None)
            data.pop("_file_name", None)
            print(json.dumps(data, indent=2, default=str))
            return 0
        if getattr(args, "cfg_cmd", None) == "save":
            if args.mission_dir:
                cfg.mission_dir = expand_path(args.mission_dir)
            if args.dcs_path:
                cfg.dcs_path = expand_path(args.dcs_path)
            cfg.save()
            print(f"Saved config to {cfg._path}")
            return 0
        if getattr(args, "cfg_cmd", None) == "delete":
            p = cfg._path
            if p.exists():
                p.unlink()
                print(f"Deleted config file {p}")
            else:
                print(f"No config file found at {p}")
            return 0
