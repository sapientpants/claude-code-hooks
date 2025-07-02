#!/usr/bin/env python3
"""
Hook to prevent git commands with --no-verify flag from being executed.
This ensures all git hooks and verification steps are properly executed.
"""

import json
import sys
import re


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Extract tool information
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        
        # Only process Bash tool calls
        if tool_name != "Bash":
            sys.exit(0)
        
        # Get the command from tool_input
        command = tool_input.get("command", "")
        
        # Check if it's a git command
        if not re.search(r'\bgit\b', command):
            sys.exit(0)
        
        # Remove quoted strings to avoid false positives
        # Remove single-quoted strings
        cleaned_cmd = re.sub(r"'[^']*'", "", command)
        # Remove double-quoted strings  
        cleaned_cmd = re.sub(r'"[^"]*"', "", cleaned_cmd)
        
        # Check for --no-verify or -n flag
        no_verify_pattern = r'(^|\s)--no-verify($|=|\s)'
        short_n_pattern = r'(^|\s)-n($|\s)'
        
        if re.search(no_verify_pattern, cleaned_cmd) or re.search(short_n_pattern, cleaned_cmd):
            # Block with error message (exit code 2)
            print("Error: Git commands with --no-verify flag are not allowed.", file=sys.stderr)
            print("This ensures all git hooks and verification steps are properly executed.", file=sys.stderr)
            print("Please run the git command without the --no-verify flag.", file=sys.stderr)
            sys.exit(2)
        
        # Allow the command to proceed
        sys.exit(0)
        
    except json.JSONDecodeError:
        # If JSON parsing fails, allow the command (fail open)
        sys.exit(0)
    except Exception as e:
        # For any other errors, allow the command (fail open)
        sys.exit(0)


if __name__ == "__main__":
    main()