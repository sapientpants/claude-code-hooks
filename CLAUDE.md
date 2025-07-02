# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the `claude-code-hooks` repository, which provides hooks for Claude Code to enforce development best practices. The hooks use Claude Code's JSON-based hook interface.

## Project Structure

```
claude-code-hooks/
├── hooks/
│   ├── claude-code-hooks.json    # Hook configuration
│   └── scripts/
│       └── block-git-no-verify.py # Hook implementation
├── tests/
│   └── test_block_git_no_verify.py # Test suite
├── run_tests.sh                    # Test runner
└── README.md                       # User documentation
```

## Development Commands

- **Run all tests**: `./run_tests.sh`
- **Run specific test**: `python3 tests/test_block_git_no_verify.py`

## Hook Development Guidelines

1. **Hook Interface**: Hooks receive JSON via stdin with:
   - `tool_name`: The Claude Code tool being called
   - `tool_input`: Tool-specific parameters
   - `session_id`: Unique session identifier
   - `transcript_path`: Path to conversation JSON

2. **Exit Codes**:
   - `0`: Allow tool execution
   - `2`: Block with error message (stderr is shown to user)
   - Other: Non-blocking error

3. **Implementation Language**: Python 3 (for reliable JSON handling)

4. **Testing**: All hooks must have comprehensive test coverage

## Important Notes

- Hooks run with full user permissions
- Always fail open (allow on error) for safety
- Test with actual Claude Code JSON interface
- Repository Remote: `git@github.com:sapientpants/claude-code-hooks.git`
- License: MIT (Copyright 2025 sapientpants)