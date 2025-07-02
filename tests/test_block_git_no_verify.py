#!/usr/bin/env python3
"""
Test script for block-git-no-verify.py hook
Tests various scenarios to ensure the hook works correctly with Claude Code's JSON interface
"""

import json
import subprocess
import sys
import os

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

# Test counters
tests_run = 0
tests_passed = 0
tests_failed = 0

# Hook script location
script_dir = os.path.dirname(os.path.abspath(__file__))
hook_script = os.path.join(script_dir, "../hooks/scripts/block-git-no-verify.py")


def run_test(test_name, command, expected_exit_code):
    """Run a single test case"""
    global tests_run, tests_passed, tests_failed
    
    tests_run += 1
    
    # Create the JSON input that Claude Code would send
    input_data = {
        "session_id": "test-session",
        "transcript_path": "/tmp/test-transcript.json",
        "tool_name": "Bash",
        "tool_input": {
            "command": command
        }
    }
    
    # Run the hook script with JSON input
    process = subprocess.Popen(
        [sys.executable, hook_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = process.communicate(input=json.dumps(input_data).encode())
    actual_exit_code = process.returncode
    
    if actual_exit_code == expected_exit_code:
        print(f"{GREEN}✓{NC} {test_name}")
        tests_passed += 1
    else:
        print(f"{RED}✗{NC} {test_name}")
        print(f"  Command: {command}")
        print(f"  Expected exit code: {expected_exit_code}, Got: {actual_exit_code}")
        if stderr:
            print(f"  Stderr: {stderr.decode().strip()}")
        tests_failed += 1


def run_non_bash_test(test_name, tool_name, expected_exit_code):
    """Test non-Bash tools (should always pass)"""
    global tests_run, tests_passed, tests_failed
    
    tests_run += 1
    
    # Create JSON input for non-Bash tool
    input_data = {
        "session_id": "test-session",
        "transcript_path": "/tmp/test-transcript.json",
        "tool_name": tool_name,
        "tool_input": {
            "content": "some content"
        }
    }
    
    process = subprocess.Popen(
        [sys.executable, hook_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = process.communicate(input=json.dumps(input_data).encode())
    actual_exit_code = process.returncode
    
    if actual_exit_code == expected_exit_code:
        print(f"{GREEN}✓{NC} {test_name}")
        tests_passed += 1
    else:
        print(f"{RED}✗{NC} {test_name}")
        print(f"  Tool: {tool_name}")
        print(f"  Expected exit code: {expected_exit_code}, Got: {actual_exit_code}")
        tests_failed += 1


def test_malformed_input():
    """Test with malformed JSON input"""
    global tests_run, tests_passed, tests_failed
    
    tests_run += 1
    
    process = subprocess.Popen(
        [sys.executable, hook_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = process.communicate(input=b"not valid json")
    actual_exit_code = process.returncode
    
    if actual_exit_code == 0:  # Should fail open
        print(f"{GREEN}✓{NC} Handle malformed JSON gracefully")
        tests_passed += 1
    else:
        print(f"{RED}✗{NC} Handle malformed JSON gracefully")
        print(f"  Expected exit code: 0, Got: {actual_exit_code}")
        tests_failed += 1


def main():
    print("Running tests for block-git-no-verify.py hook")
    print("=============================================")
    print()
    
    # Basic functionality tests
    print("Basic Functionality Tests:")
    run_test("Block: git commit --no-verify", "git commit --no-verify -m 'test'", 2)
    run_test("Block: git push --no-verify", "git push --no-verify origin main", 2)
    run_test("Block: git push with --no-verify at end", "git push origin main --no-verify", 2)
    run_test("Allow: git commit without --no-verify", "git commit -m 'test'", 0)
    run_test("Allow: git push without --no-verify", "git push origin main", 0)
    print()
    
    # Edge cases
    print("Edge Cases:")
    run_test("Block: git with multiple flags including --no-verify", 
             "git commit -a --no-verify -m 'test' --amend", 2)
    run_test("Block: Complex git command with --no-verify", 
             "git -c user.name='test' commit --no-verify -m 'msg'", 2)
    run_test("Allow: --no-verify in commit message", 
             "git commit -m 'Added --no-verify to docs'", 0)
    run_test("Allow: non-git command with --no-verify", "npm install --no-verify", 0)
    run_test("Allow: grep command searching for --no-verify", "grep --no-verify file.txt", 0)
    print()
    
    # Command variations
    print("Command Variations:")
    run_test("Block: git command with equals sign", "git commit --no-verify=true -m 'test'", 2)
    run_test("Block: git with shorthand -n", "git commit -n -m 'test'", 2)
    run_test("Allow: git status (read-only command)", "git status", 0)
    run_test("Allow: git log (read-only command)", "git log --oneline", 0)
    run_test("Allow: git diff (read-only command)", "git diff HEAD~1", 0)
    print()
    
    # Special characters and security
    print("Special Characters & Security:")
    run_test("Block: Command with special chars", "git commit --no-verify -m 'test; echo hacked'", 2)
    run_test("Block: Command with newlines", "git commit --no-verify -m 'test\\necho hacked'", 2)
    run_test("Allow: Command with quotes", 'git commit -m "test \'with\' quotes"', 0)
    run_test("Block: Command with backticks", "git commit --no-verify -m `echo test`", 2)
    print()
    
    # Non-Bash tools
    print("Non-Bash Tools (should always allow):")
    run_non_bash_test("Allow: Write tool", "Write", 0)
    run_non_bash_test("Allow: Read tool", "Read", 0)
    run_non_bash_test("Allow: Edit tool", "Edit", 0)
    print()
    
    # Error handling
    print("Error Handling:")
    test_malformed_input()
    run_test("Empty command", "", 0)
    print()
    
    # Summary
    print("=============================================")
    print("Test Summary:")
    print(f"Total tests: {tests_run}")
    print(f"Passed: {GREEN}{tests_passed}{NC}")
    print(f"Failed: {RED}{tests_failed}{NC}")
    
    if tests_failed == 0:
        print(f"\n{GREEN}All tests passed!{NC}")
        sys.exit(0)
    else:
        print(f"\n{RED}Some tests failed!{NC}")
        sys.exit(1)


if __name__ == "__main__":
    main()