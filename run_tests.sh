#!/bin/bash

# Test runner for Claude Code hooks
# This script runs all test files in the tests directory

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Claude Code Hooks Test Suite${NC}"
echo "============================"
echo

# Find all test scripts in the tests directory (both .sh and .py)
test_files=$(find tests \( -name "test_*.sh" -o -name "test_*.py" \) -type f | sort)

if [ -z "$test_files" ]; then
    echo -e "${RED}No test files found in tests directory${NC}"
    exit 1
fi

# Track overall results
all_passed=true

# Run each test file
for test_file in $test_files; do
    echo -e "${BLUE}Running: $test_file${NC}"
    
    # Determine how to run the test based on extension
    if [[ "$test_file" == *.sh ]]; then
        runner="bash"
    elif [[ "$test_file" == *.py ]]; then
        runner="python3"
    fi
    
    if $runner "$test_file"; then
        echo -e "${GREEN}✓ $test_file passed${NC}"
    else
        echo -e "${RED}✗ $test_file failed${NC}"
        all_passed=false
    fi
    echo
done

# Final summary
echo "============================"
if $all_passed; then
    echo -e "${GREEN}All test suites passed!${NC}"
    exit 0
else
    echo -e "${RED}Some test suites failed!${NC}"
    exit 1
fi