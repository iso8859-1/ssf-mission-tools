from pathlib import Path

from ssf_mission_tools.parse_lua import parse_lua_table_file


def test_parse_mission_01():
    p = Path(__file__).resolve().parents[1] / "tests" / "test_data" / "mission_01"
    data = parse_lua_table_file(p)
    # basic sanity checks
    assert isinstance(data, dict)
    assert "trig" in data
    assert "date" in data
    assert data["date"]["Year"] == 1999
