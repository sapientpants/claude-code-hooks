#!/bin/bash

# Test script for block-git-no-verify.sh hook
# This script tests various scenarios to ensure the hook works correctly

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Hook script location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOOK_SCRIPT="$SCRIPT_DIR/../hooks/scripts/block-git-no-verify.sh"

# Test function
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_exit_code="$3"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    # Set the environment variable that Claude Code would set
    export CLAUDE_TOOL_BASH_COMMAND="$command"
    
    # Run the hook script and capture exit code
    $HOOK_SCRIPT >/dev/null 2>&1
    local actual_exit_code=$?
    
    if [ $actual_exit_code -eq $expected_exit_code ]; then
        echo -e "${GREEN}✓${NC} $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $test_name"
        echo "  Command: $command"
        echo "  Expected exit code: $expected_exit_code, Got: $actual_exit_code"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

echo "Running tests for block-git-no-verify.sh hook"
echo "============================================="
echo

# Basic functionality tests
echo "Basic Functionality Tests:"
run_test "Block: git commit --no-verify" "git commit --no-verify -m 'test'" 1
run_test "Block: git push --no-verify" "git push --no-verify origin main" 1
run_test "Block: git push with --no-verify at end" "git push origin main --no-verify" 1
run_test "Allow: git commit without --no-verify" "git commit -m 'test'" 0
run_test "Allow: git push without --no-verify" "git push origin main" 0
echo

# Edge cases
echo "Edge Cases:"
run_test "Block: git with multiple flags including --no-verify" "git commit -a --no-verify -m 'test' --amend" 1
run_test "Block: Complex git command with --no-verify" "git -c user.name='test' commit --no-verify -m 'msg'" 1
run_test "Allow: --no-verify in commit message" "git commit -m 'Added --no-verify to docs'" 0
run_test "Allow: non-git command with --no-verify" "npm install --no-verify" 0
run_test "Allow: grep command searching for --no-verify" "grep --no-verify file.txt" 0
echo

# Command variations
echo "Command Variations:"
run_test "Block: git command with equals sign" "git commit --no-verify=true -m 'test'" 1
run_test "Block: git with shorthand -n" "git commit -n -m 'test'" 1
run_test "Allow: git status (read-only command)" "git status" 0
run_test "Allow: git log (read-only command)" "git log --oneline" 0
run_test "Allow: git diff (read-only command)" "git diff HEAD~1" 0
echo

# Special characters and injection attempts
echo "Special Characters & Security:"
run_test "Block: Command with special chars" "git commit --no-verify -m 'test; echo hacked'" 1
run_test "Block: Command with newlines" "git commit --no-verify -m 'test\necho hacked'" 1
run_test "Allow: Command with quotes" "git commit -m \"test 'with' quotes\"" 0
run_test "Block: Command with backticks" "git commit --no-verify -m \`echo test\`" 1
echo

# Error handling
echo "Error Handling:"
# Test with empty environment variable
unset CLAUDE_TOOL_BASH_COMMAND
$HOOK_SCRIPT >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Handle missing CLAUDE_TOOL_BASH_COMMAND gracefully"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}✗${NC} Handle missing CLAUDE_TOOL_BASH_COMMAND gracefully"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# Test with empty command
export CLAUDE_TOOL_BASH_COMMAND=""
$HOOK_SCRIPT >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Handle empty command gracefully"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}✗${NC} Handle empty command gracefully"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))
echo

# Summary
echo "============================================="
echo "Test Summary:"
echo "Total tests: $TESTS_RUN"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed!${NC}"
    exit 1
fi