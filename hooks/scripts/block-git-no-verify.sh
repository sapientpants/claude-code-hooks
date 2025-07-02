#!/bin/bash

# This hook prevents git commands with the --no-verify flag from being executed
# It's designed to enforce commit hooks and other git verification steps

# Check if the command contains 'git' and '--no-verify' or '-n' (shorthand)
if [[ "$CLAUDE_TOOL_BASH_COMMAND" =~ git ]]; then
    # Remove content within quotes to avoid false matches
    # This is a simplified approach that handles most common cases
    cleaned_cmd="$CLAUDE_TOOL_BASH_COMMAND"
    
    # Remove single-quoted strings
    cleaned_cmd=$(echo "$cleaned_cmd" | sed "s/'[^']*'//g")
    
    # Remove double-quoted strings
    cleaned_cmd=$(echo "$cleaned_cmd" | sed 's/"[^"]*"//g')
    
    # Now check for --no-verify or -n in the cleaned command
    if [[ "$cleaned_cmd" =~ (^|[[:space:]])--no-verify($|=|[[:space:]]) ]] || \
       [[ "$cleaned_cmd" =~ (^|[[:space:]])-n($|[[:space:]]) ]]; then
        echo "Error: Git commands with --no-verify flag are not allowed." >&2
        echo "This ensures all git hooks and verification steps are properly executed." >&2
        echo "Please run the git command without the --no-verify flag." >&2
        exit 1
    fi
fi

# Allow the command to proceed
exit 0