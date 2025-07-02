# Claude Code Hooks

[![Test Claude Code Hooks](https://github.com/sapientpants/claude-code-hooks/actions/workflows/test.yml/badge.svg)](https://github.com/sapientpants/claude-code-hooks/actions/workflows/test.yml)

A collection of hooks for Claude Code to enhance git workflow security and enforce best practices.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/sapientpants/claude-code-hooks.git

# Copy hooks to your project
cp -r claude-code-hooks/hooks your-project/
cd your-project

# Configure Claude Code to use the hooks
mkdir -p .claude
cp hooks/claude-code-hooks.json .claude/settings.json

# Test that it works
python3 hooks/scripts/block-git-no-verify.py < /dev/null
# Should exit without error
```

## Requirements

- **Python 3.6 or higher** - Check your version with `python3 --version`
  - macOS: Pre-installed
  - Ubuntu/Debian: `sudo apt-get install python3`
  - Windows: Download from [python.org](https://www.python.org/downloads/)
- **Claude Code CLI** - The hooks are designed to work with Claude Code

## Overview

This repository provides pre-configured hooks for Claude Code that help enforce development standards and prevent potentially unsafe operations.

## Available Hooks

### Block Git No-Verify

**Purpose**: Prevents execution of git commands that include the `--no-verify` flag, ensuring that all git hooks and verification steps are properly executed.

**What it blocks**:
- `git commit --no-verify`
- `git push --no-verify`
- Any git command containing the `--no-verify` flag

**Why**: The `--no-verify` flag bypasses important git hooks that may perform:
- Code linting
- Test execution
- Commit message validation
- Security checks
- Code formatting

## Installation

### Prerequisites Check
First, ensure Python is available:
```bash
python3 --version
# Should show Python 3.6 or higher
```

### Method 1: Project-specific installation (Recommended)
1. Clone this repository or download the `hooks` directory
2. Copy the `hooks` directory to your project root
3. Add the hook configuration to your project's Claude Code settings:

```bash
# Create .claude directory if it doesn't exist
mkdir -p .claude

# Copy the hook configuration
cp hooks/claude-code-hooks.json .claude/settings.json
```

Or manually add to `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./hooks/scripts/block-git-no-verify.py"
          }
        ]
      }
    ]
  }
}
```

### Method 2: User-level installation
1. Copy the hooks to your home directory:
```bash
cp -r hooks ~/.claude-hooks
```

2. Add to your user settings at `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude-hooks/scripts/block-git-no-verify.py"
          }
        ]
      }
    ]
  }
}
```


## Usage

Once installed, the hooks will automatically run when Claude Code attempts to execute matching commands. If a blocked pattern is detected, the command will be prevented from executing and an informative error message will be displayed.

### Example

When Claude Code attempts to run:
```bash
git commit --no-verify -m "Skip checks"
```

The hook will block execution and display:
```
Error: Git commands with --no-verify flag are not allowed.
This ensures all git hooks and verification steps are properly executed.
Please run the git command without the --no-verify flag.
```

## Testing

Run the test suite to verify the hooks work correctly:

```bash
./run_tests.sh
```

To test a specific hook:
```bash
./tests/test_block_git_no_verify.py
```

## Troubleshooting

### "python3: command not found"
- Install Python 3 using the instructions in the Requirements section
- On some systems, try `python` instead of `python3`

### Hook not triggering
1. Check if the hook is loaded in Claude Code:
   ```
   /hooks
   ```
   
2. Verify Python can run the script:
   ```bash
   python3 hooks/scripts/block-git-no-verify.py < /dev/null
   ```
   
3. Ensure the path in `.claude/settings.json` is correct (relative to your project root)

### "Permission denied" error
```bash
chmod +x hooks/scripts/block-git-no-verify.py
```

## How It Works

The hook configuration in `.claude/settings.json` tells Claude Code to run `block-git-no-verify.py` before executing any Bash commands. The Python script:

1. Receives the command details from Claude Code as JSON
2. Checks if it's a git command with `--no-verify` 
3. Blocks the command if found, allows it otherwise

## Contributing

Feel free to submit issues or pull requests for additional hooks that enhance development security and best practices.

## License

MIT License - see LICENSE file for details.