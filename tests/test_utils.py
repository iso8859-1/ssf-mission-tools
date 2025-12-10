import tempfile
import zipfile
from pathlib import Path

from ssf_mission_tools.utils import unzip


def test_unzip_basic(tmp_path: Path):
    # create a zip file
    zpath = tmp_path / "test.zip"
    with zipfile.ZipFile(zpath, "w") as z:
        z.writestr("a.txt", "hello")
        z.writestr("sub/b.txt", "world")

    dest = tmp_path / "out"
    unzip(zpath, dest)

    assert (dest / "a.txt").read_text() == "hello"
    assert (dest / "sub" / "b.txt").read_text() == "world"


def test_unzip_prevents_zip_slip(tmp_path: Path):
    zpath = tmp_path / "evil.zip"
    with zipfile.ZipFile(zpath, "w") as z:
        # path that would traverse out of dest
        z.writestr("../evil.txt", "bad")

    dest = tmp_path / "out2"
    try:
        unzip(zpath, dest)
        assert False, "zip slip should have been detected"
    except ValueError:
        # expected
        pass
