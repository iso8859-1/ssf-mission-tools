# SSF Mission Tools - Usage Guide

This guide provides comprehensive instructions for using the SSF Mission Tools command-line interface.

## Installation

### Installing from Source

To install the package in development mode:

```powershell
pip install -e .
```

After installation, the `ssf-tools` command will be available on your PATH.

### Running Without Installation

You can run the tool directly from the source directory without installing:

```powershell
python -m ssf_mission_tools [command]
```

## Command Overview

The SSF Mission Tools CLI uses a git-style command structure with subcommands. All commands follow this pattern:

```
ssf-tools <command> [subcommand] [options]
```

### Available Commands

- `config` - Manage application configuration
- `init` - Initialize a development directory for mission editing
- `update` - Update mission files in the development directory from DCS
- `build` - Build a .miz file from the development directory
- `--version` - Display the application version

---

## Configuration Management

The `config` command manages persistent application settings stored in a JSON configuration file.

### Configuration File Location

The configuration file is stored in a platform-specific user directory:

- **Windows**: `%APPDATA%\ssf-mission-tools\ssf-mission-tools.config.json`
- **Linux/macOS**: `~/.config/ssf-mission-tools/ssf-mission-tools.config.json`

### Configuration Settings

The following settings are available:

| Setting | Description | Default Value |
|---------|-------------|---------------|
| `mission_dir` | Path to your DCS missions directory | Auto-detected from DCS Saved Games |
| `dcs_path` | Path to your DCS World installation | `C:/Program Files/Eagle Dynamics/DCS World` |

### Viewing Current Configuration

Display all current configuration settings:

```powershell
ssf-tools config show
```

**Example Output:**
```json
{
  "mission_dir": "C:/Users/YourName/Saved Games/DCS/Missions",
  "dcs_path": "C:/Program Files/Eagle Dynamics/DCS World"
}
```

### Modifying Configuration

Change one or more configuration settings and save to disk:

```powershell
ssf-tools config save --mission-dir "D:/My DCS Missions" --dcs-path "D:/DCS"
```

You can update individual settings:

```powershell
# Update only the mission directory
ssf-tools config save --mission-dir "~/Documents/DCS/Missions"

# Update only the DCS installation path
ssf-tools config save --dcs-path "C:/Program Files/DCS World OpenBeta"
```

**Notes:**
- Paths support environment variables (e.g., `%USERPROFILE%`, `$HOME`)
- Tilde (`~`) expands to your home directory
- Paths are automatically normalized to use forward slashes internally

### Deleting Configuration

Remove the configuration file and revert to default settings:

```powershell
ssf-tools config delete
```

If no configuration file exists, you'll see:
```
No config file found at [path]
```

---

## Mission Workflow Commands

### Initialize Development Directory

The `init` command sets up a new development directory for mission editing:

```powershell
ssf-tools init [options]
```

**Options:**
- (To be documented once implemented)

### Update Mission Files

The `update` command synchronizes your development directory with changes from the DCS mission file:

```powershell
ssf-tools update [options]
```

**Options:**
- (To be documented once implemented)

### Build Mission Package

The `build` command creates a `.miz` file from your development directory:

```powershell
ssf-tools build [options]
```

**Options:**
- (To be documented once implemented)

---

## Common Usage Examples

### First-Time Setup

1. Install the tool:
   ```powershell
   pip install -e .
   ```

2. Check the default configuration:
   ```powershell
   ssf-tools config show
   ```

3. If needed, update paths to match your installation:
   ```powershell
   ssf-tools config save --dcs-path "D:/DCS World" --mission-dir "D:/Missions"
   ```

### Typical Workflow

```powershell
# 1. Initialize a new mission development directory
ssf-tools init --mission MyMission.miz

# 2. Make changes to your mission files...

# 3. Build the updated .miz file
ssf-tools build

# 4. Update from DCS if the mission was modified in-game
ssf-tools update
```

---

## Getting Help

Display general help:

```powershell
ssf-tools --help
```

Display help for a specific command:

```powershell
ssf-tools config --help
ssf-tools init --help
```

Display help for a subcommand:

```powershell
ssf-tools config save --help
```

---

## Troubleshooting

### Configuration Not Persisting

If configuration changes don't persist:
1. Verify the config directory exists and is writable
2. Check file permissions on the configuration file
3. Run `ssf-tools config show` to verify current settings

### Path Not Found Errors

If you encounter path-related errors:
1. Ensure paths in the configuration use forward slashes or are properly escaped
2. Verify the paths exist on your system
3. Use `ssf-tools config show` to check current path settings
4. Update paths with `ssf-tools config save --mission-dir "correct/path"`

### Command Not Found

If `ssf-tools` command is not recognized:
- Ensure the package is installed: `pip install -e .`
- Verify your Python Scripts directory is on your PATH
- As an alternative, use: `python -m ssf_mission_tools [command]`

---

## Advanced Usage

### Environment Variables in Paths

You can use environment variables in configuration paths:

```powershell
ssf-tools config save --mission-dir "%USERPROFILE%/Documents/DCS/Missions"
```

On Linux/macOS:
```bash
ssf-tools config save --mission-dir "$HOME/Documents/DCS/Missions"
```

### Scripting and Automation

The tool returns exit codes that can be used in scripts:
- `0` - Success
- `1` - General error
- `-1` - Specific failure (e.g., file not found)

Example PowerShell script:
```powershell
ssf-tools config show
if ($LASTEXITCODE -eq 0) {
    Write-Host "Configuration loaded successfully"
} else {
    Write-Host "Failed to load configuration"
    exit 1
}
```
