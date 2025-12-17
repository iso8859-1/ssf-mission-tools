"""Helpers to parse Lua table-literal files commonly found in DCS missions.

This module provides a best-effort extractor that locates a top-level table
assignment (for example `mission = { ... }` or a trailing `return { ... }`) and
decodes it into Python using `slpp`.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from slpp import slpp as lua


_TABLE_RE_RETURN = re.compile(r"return\s+({.*})\s*$", re.S)
_TABLE_RE_ASSIGN = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*({.*})", re.S)


def _find_table_literal(text: str) -> str | None:
    # Try trailing return { ... }
    m = _TABLE_RE_RETURN.search(text)
    if m:
        return m.group(1)
    # Note: assignment pattern is handled in the main parser to capture the
    # variable name. Here we only look for a trailing `return { ... }` and
    # fallback to a naive brace block search.
    # Last resort: find the first large brace block (naive)
    m = re.search(r"({\s*\n.*\n})", text, re.S)
    if m:
        return m.group(1)
    return None


def parse_lua_table_file(path: str | Path) -> Any:
    p = Path(path)
    txt = p.read_text(encoding="utf-8", errors="ignore")
    # detect assignment with variable name first; capture both the name and the table
    m = _TABLE_RE_ASSIGN.search(txt)
    if m:
        varname = m.group(1)
        tbl = m.group(2)
        data = lua.decode(tbl)
        return {"variable": varname, "data": data}

    tbl = _find_table_literal(txt)
    if not tbl:
        raise ValueError(f"No top-level table literal found in {p}")
    # slpp expects a Lua table expression; decode to Python
    data = lua.decode(tbl)
    return {"variable": None, "data": data}

def sort_and_write(variable: str | None, data: Any, path: str | Path) -> None:
    """Sort a Lua table and write it back to file.

    This function sorts dictionary keys by a natural-order key derived from
    the string representation of each key (so numeric substrings sort
    numerically: "1","2","10" -> 1,2,10). Works with mixed string/number keys.
    """
    def natural_key(k: Any):
        s = str(k)
        parts = re.split(r'(\d+)', s)
        key_parts = []
        for part in parts:
            if not part:
                continue
            if part.isdigit():
                key_parts.append((0, int(part)))
            else:
                key_parts.append((1, part.lower()))
        return tuple(key_parts)

    def sort_table(obj: Any) -> Any:
        if isinstance(obj, dict):
            items = sorted(obj.items(), key=lambda kv: natural_key(kv[0]))
            return {k: sort_table(v) for k, v in items}
        elif isinstance(obj, list):
            return [sort_table(item) for item in obj]
        else:
            return obj

    sorted_data = sort_table(data)
    lua_table_str = lua.encode(sorted_data)
    with open(path, "w", encoding="utf-8") as f:
        if variable:
            f.write(f"{variable} = {lua_table_str}\n")
        else:
            f.write(f"{lua_table_str}\n")