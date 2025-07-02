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

1. Clone this repository or copy the hooks directory to your project
2. Configure Claude Code to use the hooks by either:
   - Setting the `CLAUDE_CODE_HOOKS_DIR` environment variable to point to the hooks directory
   - Copying the hook configuration to your Claude Code settings directory

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

## Configuration

The hooks are configured in `hooks/claude-code-hooks.json`. The configuration uses Claude Code's hook system to run validation scripts before tool execution.

## Contributing

Feel free to submit issues or pull requests for additional hooks that enhance development security and best practices.

## License

MIT License - see LICENSE file for details.