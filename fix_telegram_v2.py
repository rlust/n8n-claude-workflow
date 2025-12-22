#!/usr/bin/env python3
"""Fix the Telegram Response node - download fresh from API and update"""
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

print("🔧 Fixing Telegram Response node\n")
print("=" * 70)

# Download workflow fresh from API
print("\n📥 Downloading workflow from n8n API...")
get_response = requests.get(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers
)

if get_response.status_code != 200:
    print(f"❌ Failed to get workflow: {get_response.status_code}")
    exit(1)

workflow = get_response.json()
print(f"✅ Downloaded workflow: {workflow['name']}")

# Find and update Telegram Response node
node_found = False
for node in workflow['nodes']:
    if node['name'] == 'Telegram Response':
        print(f"\n✅ Found Telegram Response node")

        assignments = node['parameters']['assignments']['assignments']

        # Find the telegram_message_id assignment
        for assignment in assignments:
            if assignment['name'] == 'telegram_message_id':
                print(f"\n📋 Current configuration:")
                print(f"   Expression: {assignment['value']}")

                # Update the expression
                old_value = assignment['value']
                assignment['value'] = "={{ $json.result.message_id }}"

                print(f"\n📝 Updated configuration:")
                print(f"   Old: {old_value}")
                print(f"   New: {assignment['value']}")

                node_found = True
        break

if not node_found:
    print("❌ Telegram Response node not found!")
    exit(1)

# Prepare update payload - only include allowed fields
print(f"\n" + "=" * 70)
print(f"🚀 Updating workflow...")

# Remove read-only fields
workflow_update = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections']
}

# Optionally include settings if present
if 'settings' in workflow and workflow['settings']:
    # Only include specific allowed settings fields
    allowed_settings = {}
    if 'executionOrder' in workflow['settings']:
        allowed_settings['executionOrder'] = workflow['settings']['executionOrder']
    if 'saveDataErrorExecution' in workflow['settings']:
        allowed_settings['saveDataErrorExecution'] = workflow['settings']['saveDataErrorExecution']
    if 'saveDataSuccessExecution' in workflow['settings']:
        allowed_settings['saveDataSuccessExecution'] = workflow['settings']['saveDataSuccessExecution']
    if 'saveManualExecutions' in workflow['settings']:
        allowed_settings['saveManualExecutions'] = workflow['settings']['saveManualExecutions']

    if allowed_settings:
        workflow_update['settings'] = allowed_settings

# Include staticData if present
if 'staticData' in workflow:
    workflow_update['staticData'] = workflow['staticData']

response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json=workflow_update
)

if response.status_code == 200:
    print(f"✅ Workflow updated successfully!")
    print(f"\n✨ Fixed: telegram_message_id now uses $json.result.message_id")
    print(f"\n🎉 Test the workflow to confirm message_id is now captured!")
else:
    print(f"❌ Failed to update workflow: {response.status_code}")
    print(f"Response: {response.text}")

print("\n" + "=" * 70)
