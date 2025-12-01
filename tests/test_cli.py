import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def run_module(argv):
    cmd = [sys.executable, "-m", "ssf_mission_tools"] + argv
    p = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

def test_help():
    rc, out, err = run_module(["--help"])
    assert rc != 0
    assert "usage" in out.lower() or "usage" in err.lower()

def test_hello():
    rc, out, err = run_module(["hello", "--name", "TestUser"])
    assert rc == 0
    assert "Hello, TestUser!" in out
