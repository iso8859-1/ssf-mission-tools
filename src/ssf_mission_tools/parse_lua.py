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
_TABLE_RE_ASSIGN = re.compile(r"^\s*mission\s*=\s*({.*})\s*$", re.S | re.M)


def _find_table_literal(text: str) -> str | None:
    # Try trailing return { ... }
    m = _TABLE_RE_RETURN.search(text)
    if m:
        return m.group(1)
    # Try assignment like: mission = { ... }
    m = _TABLE_RE_ASSIGN.search(text)
    if m:
        return m.group(1)
    # Last resort: find the first large brace block (naive)
    m = re.search(r"({\s*\n.*\n})", text, re.S)
    if m:
        return m.group(1)
    return None


def parse_lua_table_file(path: str | Path) -> Any:
    p = Path(path)
    txt = p.read_text(encoding="utf-8", errors="ignore")
    tbl = _find_table_literal(txt)
    if not tbl:
        raise ValueError(f"No top-level table literal found in {p}")
    # slpp expects a Lua table expression; decode to Python
    return lua.decode(tbl)
