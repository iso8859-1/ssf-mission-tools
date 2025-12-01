# ssf-mission-tools

This package contains scripts that support during mission generation in DCS. They are designed to allow a workflow that supports git for version control and dynamic loading of scripts during the development process.

## Workflow

The scripts are built to follow a certain workflow.

1. A skeleton mission needs to be created in Step 0
2. the directory needs to be initialized with `--init`

The following steps are the main development workflow and can be done in any order

a) Change the mission in DCS and update the development directory with `--update`
b) Create a miz-file based on the contents of the development directory with `--build`

### Step 0

Create an empty mission with the desired name, map & factions in DCS and save it.

### init

The init command prepares the development directory.

These are the steps that are performed during initialization:

- creation of the directory-structure
- initialization of a git repo
- initialization of the mission data from an existing mission
- add MOOSE to the mission

### update

Update works similar to step 0. It copies the contents of the current miz file into the development directory. During that process it ensures that only meaningful changes are copied. This ensures that the diff that git offers provides meaningful information about the change.

Transformation done by update:
- sorting of the lua-tables
- mark scripts for dynamic loading

### build

Build collects the information in the development folder and constructs a runneable miz file. There are 2 flavors of build `dev` and `release`. The dev-build keeps the script files in the development folder and does **not** embed them into the `.miz` file. This is ideal for development. The scripts can be changed directly in the development folder and in DCS, the developer just needs to restart the mission to see the effect of the update. The release-build embeds the scripts into the miz file. This allows easy distribution.

## run instructions

Command-line utilities and GUI tools for SSF mission workflows.

Run the CLI:

```powershell
python -m ssf_mission_tools --help
```

Run the GUI stub (if tkinter is available):

```powershell
python -c "import ssf_mission_tools.gui.app as g; g.run_app()"
```

Run tests (from project root):

```powershell
python -m pytest -q
```

Build a standalone Windows exe with PyInstaller

Install dev deps and build (PowerShell):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
python -m pip install -r requirements-dev.txt
.\scripts\build-pyinstaller.ps1
```

The produced executable will be in `dist\ssf-tools.exe`.

