#!/usr/bin/env python3
"""Change PNB to PRK in the workflow"""
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
WORKFLOW_ID = os.getenv('WORKFLOW_ID_STOCK_TO_TELEGRAM_V3')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("🔧 Changing PNB to PRK in workflow\n")
print("=" * 70)

# Download current workflow
print("\n📥 Downloading current workflow...")
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)

if response.status_code != 200:
    print(f"❌ Failed to download: {response.status_code}")
    exit(1)

workflow = response.json()
print(f"✅ Downloaded: {workflow['name']}")

# Search and replace PNB with PRK in all nodes
print("\n🔍 Searching for PNB references...")
changes_made = False

for node in workflow['nodes']:
    node_changed = False

    # Convert node to string to check for PNB
    node_str = json.dumps(node)

    if 'PNB' in node_str:
        print(f"\n📍 Found PNB in node: {node['name']}")

        # Check in parameters
        if 'parameters' in node:
            params_str = json.dumps(node['parameters'])
            if 'PNB' in params_str:
                # Replace PNB with PRK in the entire parameters object
                params_str = params_str.replace('PNB', 'PRK')
                node['parameters'] = json.loads(params_str)
                node_changed = True
                print(f"   ✅ Replaced PNB with PRK in parameters")

        # Check in other fields
        for key in node:
            if isinstance(node[key], str) and 'PNB' in node[key]:
                node[key] = node[key].replace('PNB', 'PRK')
                node_changed = True
                print(f"   ✅ Replaced PNB with PRK in {key}")

        if node_changed:
            changes_made = True

if not changes_made:
    print("\n⚠️  No PNB references found in workflow")
    print("   The stock symbol might be set elsewhere or dynamically")
    exit(0)

# Update workflow
print("\n" + "=" * 70)
print("🚀 Saving updated workflow...")

workflow_update = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections']
}

# Include settings if present
if 'settings' in workflow and workflow['settings']:
    allowed_settings = {}
    if 'executionOrder' in workflow['settings']:
        allowed_settings['executionOrder'] = workflow['settings']['executionOrder']
    if allowed_settings:
        workflow_update['settings'] = allowed_settings

# Include staticData if present
if 'staticData' in workflow:
    workflow_update['staticData'] = workflow['staticData']

update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json=workflow_update
)

if update_response.status_code == 200:
    print(f"✅ Workflow updated successfully!")
    print(f"\n✨ All PNB references changed to PRK")

    # Save to local file as well
    with open('current_workflow.json', 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"💾 Saved to current_workflow.json")
else:
    print(f"❌ Failed to update: {update_response.status_code}")
    print(f"Response: {update_response.text}")

print("\n" + "=" * 70)
