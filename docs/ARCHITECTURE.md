SSF Mission Tools - Architecture

Overview
- `src/ssf_mission_tools`: package source
  - `cli.py`: argparse-based CLI entrypoints
  - `__main__.py`: module entry to run `python -m ssf_mission_tools`
  - `gui/app.py`: tkinter-based GUI stub

Testing
- Tests live under `tests/` and use the module-runner to exercise the CLI.

Future
- Add an actual GUI framework (PySide6 or Qt) behind a feature flag
- Add subpackages for mission parsing, telemetry, export, etc.
