#!/usr/bin/env python3
"""Fix the Telegram Response node to correctly extract message_id"""
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

# Load current workflow
with open('current_workflow.json', 'r') as f:
    workflow = json.load(f)

# Find and update Telegram Response node
for node in workflow['nodes']:
    if node['name'] == 'Telegram Response':
        print(f"\n✅ Found Telegram Response node")

        assignments = node['parameters']['assignments']['assignments']

        # Find the telegram_message_id assignment
        for assignment in assignments:
            if assignment['name'] == 'telegram_message_id':
                print(f"\n📋 Current configuration:")
                print(f"   Name: {assignment['name']}")
                print(f"   Current expression: {assignment['value']}")

                # Update the expression
                assignment['value'] = "={{ $json.result.message_id }}"

                print(f"\n📝 Updated configuration:")
                print(f"   Name: {assignment['name']}")
                print(f"   New expression: {assignment['value']}")
        break

# Update workflow via API
print(f"\n" + "=" * 70)
print(f"🚀 Updating workflow {WORKFLOW_ID}...")

# Clean workflow data - remove fields that shouldn't be in PUT request
workflow_update = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections'],
    'settings': workflow.get('settings', {}),
    'staticData': workflow.get('staticData'),
    'tags': workflow.get('tags', [])
}

response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json=workflow_update
)

if response.status_code == 200:
    print(f"✅ Workflow updated successfully!")
    print(f"\n✨ The Telegram Response node now correctly extracts:")
    print(f"   telegram_message_id from $json.result.message_id")
    print(f"\n🎉 Telegram messages should now report the correct message_id!")
else:
    print(f"❌ Failed to update workflow: {response.status_code}")
    print(f"Response: {response.text}")

print("\n" + "=" * 70)
