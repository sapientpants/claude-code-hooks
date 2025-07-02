# Claude Code Hooks

[![Test Claude Code Hooks](https://github.com/sapientpants/claude-code-hooks/actions/workflows/test.yml/badge.svg)](https://github.com/sapientpants/claude-code-hooks/actions/workflows/test.yml)

A collection of hooks for Claude Code to enhance git workflow security and enforce best practices.

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

### Method 1: Project-specific installation (Recommended)
1. Copy the `hooks` directory to your project root
2. Add the hook configuration to your project's Claude Code settings:

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
            "command": "./hooks/scripts/block-git-no-verify.sh"
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
            "command": "~/.claude-hooks/scripts/block-git-no-verify.sh"
          }
        ]
      }
    ]
  }
}
```

### Method 3: Using Claude Code's /hooks command
You can also configure hooks interactively using Claude Code's `/hooks` slash command.

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
./tests/test_block_git_no_verify.sh
```

## Troubleshooting

### Hook not triggering
1. Verify the hook configuration is loaded:
   - Check `~/.claude/settings.json` or `.claude/settings.json`
   - Use the `/hooks` command in Claude Code to view active hooks

2. Ensure the hook script is executable:
   ```bash
   chmod +x hooks/scripts/block-git-no-verify.sh
   ```

3. Check the hook script path is correct in your settings

### Permission errors
- Hooks run with your user permissions
- Ensure the hook scripts have execute permissions
- Use absolute paths if relative paths aren't working

## Configuration

The hooks are configured in `hooks/claude-code-hooks.json`. The configuration uses Claude Code's hook system to run validation scripts before tool execution.

### Configuration Structure
- **Event**: `PreToolUse` - Runs before the tool executes
- **Matcher**: `Bash` - Applies to bash commands
- **Command**: Path to the hook script to execute

## Security Considerations

- Hooks run with full user permissions
- Always review hook scripts before installation
- Be cautious with hooks from untrusted sources
- Test hooks in a safe environment first

## Contributing

Feel free to submit issues or pull requests for additional hooks that enhance development security and best practices.

## License

MIT License - see LICENSE file for details.