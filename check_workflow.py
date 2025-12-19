#!/usr/bin/env python3
"""Download and check current workflow from n8n"""
import requests
import json
import os

# Load environment
N8N_API_KEY = ""
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('N8N_API_KEY='):
            N8N_API_KEY = line.split('=', 1)[1].strip()
            break

headers = {"X-N8N-API-KEY": N8N_API_KEY}
response = requests.get(
    "http://100.82.85.95:5678/api/v1/workflows/B96iHmEjsX6Yo3IM",
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    workflow = data.get('data', data)

    # Save to file
    with open('/tmp/current_workflow.json', 'w') as f:
        json.dump(workflow, f, indent=2)

    # Check for Extract Params references
    workflow_str = json.dumps(workflow)
    if "$('Extract Params')" in workflow_str:
        print("❌ Found $('Extract Params') references in workflow:")
        lines = workflow_str.split('\\n')
        for i, line in enumerate(lines):
            if "Extract Params" in line and '"name"' not in line and '"node"' not in line:
                print(f"   Line {i}: {line[:100]}")
    else:
        print("✅ No $('Extract Params') references found in expressions")
else:
    print(f"Error: {response.status_code}")
