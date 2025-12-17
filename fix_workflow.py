#!/usr/bin/env python3
"""Fix workflow by deactivating, updating, and reactivating"""
import requests
import json
import os
import time

# Load environment
N8N_API_KEY = ""
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('N8N_API_KEY='):
            N8N_API_KEY = line.split('=', 1)[1].strip()
            break

N8N_URL = "http://100.82.85.95:5678"
WORKFLOW_ID = "B96iHmEjsX6Yo3IM"
headers = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}

print("Step 1: Getting current workflow...")
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)
if response.status_code != 200:
    print(f"❌ Failed to get workflow: {response.status_code}")
    exit(1)

current = response.json().get('data', response.json())
print(f"   Current active status: {current.get('active')}")

print("\nStep 2: Deactivating workflow...")
payload = {
    "name": current.get("name"),
    "nodes": current.get("nodes"),
    "connections": current.get("connections"),
    "settings": current.get("settings", {}),
    "staticData": current.get("staticData"),
    "active": False
}
response = requests.put(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers, json=payload)
if response.status_code == 200:
    print("   ✅ Workflow deactivated")
else:
    print(f"   ⚠️  Deactivation returned: {response.status_code}")

time.sleep(1)

print("\nStep 3: Loading updated workflow from file...")
with open('n8n-workflows/examples/claude-stock-to-telegram-v3-scheduled.json', 'r') as f:
    workflow_data = json.load(f)

# Check for Extract Params references in file
workflow_str = json.dumps(workflow_data)
if "$('Extract Params')" in workflow_str:
    count = workflow_str.count("$('Extract Params')")
    print(f"   ⚠️  File still contains {count} references to $('Extract Params')")
    # Find and show them
    if "symbol1" in workflow_str and "Extract Params" in workflow_str:
        print("   Found in response body - need to fix!")
else:
    print("   ✅ File has no $('Extract Params') references")

print("\nStep 4: Updating workflow...")
payload = {
    "name": workflow_data.get("name"),
    "nodes": workflow_data.get("nodes"),
    "connections": workflow_data.get("connections"),
    "settings": workflow_data.get("settings", {}),
    "staticData": workflow_data.get("staticData"),
    "active": False
}
response = requests.put(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers, json=payload)
if response.status_code == 200:
    print("   ✅ Workflow updated")
else:
    print(f"   ❌ Update failed: {response.status_code}")
    print(f"   Response: {response.text[:500]}")
    exit(1)

time.sleep(1)

print("\nStep 5: Reactivating workflow...")
payload["active"] = True
response = requests.put(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers, json=payload)
if response.status_code == 200:
    print("   ✅ Workflow reactivated")
else:
    print(f"   ❌ Reactivation failed: {response.status_code}")
    exit(1)

print("\nStep 6: Verifying fix...")
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)
if response.status_code == 200:
    current = response.json().get('data', response.json())
    current_str = json.dumps(current)
    if "$('Extract Params')" in current_str and "symbol1" in current_str:
        print("   ❌ Workflow still has Extract Params references")
    else:
        print("   ✅ Workflow fixed!")
else:
    print(f"   ❌ Could not verify: {response.status_code}")
