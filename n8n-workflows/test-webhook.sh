#!/bin/bash

# Test script for n8n Claude workflows
# Make sure your workflows are active in n8n first!

echo "Testing Claude Code Analyzer Webhook..."
echo "========================================"
echo ""

# Test 1: Simple JavaScript code
echo "Test 1: Analyzing JavaScript code..."
curl -X POST http://localhost:5678/webhook/analyze-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "function calculateSum(a, b) { return a + b; }",
    "language": "javascript",
    "analysis_type": "review"
  }' | jq '.'

echo ""
echo ""

# Test 2: Python code with potential issues
echo "Test 2: Analyzing Python code with issues..."
curl -X POST http://localhost:5678/webhook/analyze-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def process_data(data):\n    result = []\n    for i in range(len(data)):\n        result.append(data[i] * 2)\n    return result",
    "language": "python",
    "analysis_type": "review"
  }' | jq '.'

echo ""
echo ""
echo "Tests completed!"
