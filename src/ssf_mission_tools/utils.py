from __future__ import annotations

from pathlib import Path
import zipfile
import os
from typing import Iterable


def _is_within_directory(directory: Path, target: Path) -> bool:
    try:
        directory = directory.resolve()
        target = target.resolve()
        return str(target).startswith(str(directory))
    except Exception:
        return False


def unzip(zip_path: str | Path, dest_dir: str | Path, members: Iterable[str] | None = None) -> None:
    """Safely extract a zip archive to `dest_dir`.

    This function verifies each member path to prevent zip-slip attacks.
    """
    zip_path = Path(zip_path)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as z:
        namelist = members if members is not None else z.namelist()
        for member in namelist:
            member_path = dest_dir.joinpath(member)
            if not _is_within_directory(dest_dir, member_path):
                raise ValueError(f"Unsafe path in zip archive: {member}")
        z.extractall(path=dest_dir, members=namelist)
