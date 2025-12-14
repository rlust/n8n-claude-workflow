#!/bin/bash

# Test script for Claude Agent SDK workflows in n8n
# Make sure your Agent SDK workflows are active in n8n first!

echo "=========================================="
echo "Claude Agent SDK Workflow Tests"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Find TODO comments
echo -e "${BLUE}Test 1: Finding TODO comments in codebase...${NC}"
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find all TODO, FIXME, and HACK comments in the codebase. List them with file names and line numbers.",
    "repository_path": "/tmp",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'

echo ""
echo ""

# Test 2: List files by type
echo -e "${BLUE}Test 2: Analyzing file types in directory...${NC}"
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "List all files in /tmp and categorize them by file type (extension). Count how many files of each type exist.",
    "repository_path": "/tmp",
    "allowed_tools": ["Bash", "Glob"]
  }'

echo ""
echo ""

# Test 3: Security scan
echo -e "${BLUE}Test 3: Running security scan for hardcoded secrets...${NC}"
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Search for potential security issues: hardcoded API keys, passwords, or secrets. Look for patterns like api_key, password, secret, token in the code.",
    "repository_path": "/tmp",
    "allowed_tools": ["Read", "Grep", "Glob"]
  }'

echo ""
echo ""

# Test 4: Simple directory listing
echo -e "${BLUE}Test 4: Simple directory exploration...${NC}"
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "List the contents of /tmp directory and provide a brief description of what you find.",
    "repository_path": "/tmp",
    "allowed_tools": ["Bash", "Read"]
  }'

echo ""
echo ""

# Test 5: Code quality check
echo -e "${BLUE}Test 5: Code quality analysis...${NC}"
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyze JavaScript or Python files for code quality issues: 1) Functions longer than 50 lines, 2) Missing error handling, 3) Console.log or print statements that should be removed.",
    "repository_path": "/tmp",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'

echo ""
echo ""

echo -e "${GREEN}=========================================="
echo "All tests completed!"
echo -e "==========================================${NC}"
echo ""
echo "Check the responses above to see what the agent found."
echo ""
echo "Tips:"
echo "  - The agent autonomously uses tools (Read, Bash, Glob, Grep)"
echo "  - Each test shows multi-step autonomous execution"
echo "  - Review n8n execution logs for detailed tool usage"
echo ""
