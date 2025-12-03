import os
from pathlib import Path

def expand_path(path_str: str) -> str:
    expanded = os.path.expandvars(path_str)
    return Path(expanded).expanduser().as_posix()