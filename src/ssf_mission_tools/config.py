"""Configuration helper for ssf_mission_tools.

Implements a Config dataclass with defaults, load/save to a JSON file
in the user's config directory (per-platform).
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict


def _user_config_dir(app_name: str) -> Path:
    # Follow XDG on *nix, use %APPDATA% on Windows, fallback to home
    if os.name == "nt":
        base = os.getenv("APPDATA") or Path.home() / "AppData" / "Roaming"
    else:
        base = os.getenv("XDG_CONFIG_HOME") or Path.home() / ".config"
    return Path(base) / app_name


@dataclass
class Config:
    dcs_path: str = "C:/Program Files/Eagle Dynamics/DCS World"
    mission_dir: str = "%USERPROFILE%/Saved Games/DCS/Missions"
    #extra: Dict[str, Any] = field(default_factory=dict)

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
