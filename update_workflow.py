#!/usr/bin/env python3
"""Update existing workflow in n8n"""
import requests
import json
import os

# Load environment variables
N8N_URL = os.getenv("N8N_URL", "http://100.82.85.95:5678")
N8N_API_KEY = os.getenv("N8N_API_KEY")
WORKFLOW_ID = "B96iHmEjsX6Yo3IM"
WORKFLOW_FILE = "n8n-workflows/examples/claude-stock-to-telegram-v3-scheduled.json"

if not N8N_API_KEY:
    # Read from .env file
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('N8N_API_KEY='):
                N8N_API_KEY = line.split('=', 1)[1].strip()
                break

headers = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}

# Load workflow
with open(WORKFLOW_FILE, 'r') as f:
    workflow_data = json.load(f)

# Prepare payload (exclude read-only fields)
payload = {
    "name": workflow_data.get("name"),
    "nodes": workflow_data.get("nodes"),
    "connections": workflow_data.get("connections"),
    "settings": workflow_data.get("settings", {}),
    "staticData": workflow_data.get("staticData")
}

print(f"Updating workflow {WORKFLOW_ID}...")
response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json=payload,
    timeout=30
)

if response.status_code == 200:
    print("✅ Workflow updated successfully!")
    result = response.json()
    if 'data' in result:
        print(f"   Workflow name: {result['data'].get('name')}")
        print(f"   Active: {result['data'].get('active')}")
    else:
        print(f"   Workflow name: {result.get('name')}")
        print(f"   Active: {result.get('active')}")
else:
    print(f"❌ Failed to update workflow: {response.status_code}")
    print(f"   Response: {response.text[:500]}")
