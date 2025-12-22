#!/usr/bin/env python3
"""Add 9:30 AM cron trigger to Finnhub workflow"""
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
WORKFLOW_ID = os.getenv('WORKFLOW_ID_FINNHUB_WORKING')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("🕘 Adding 9:30 AM Cron Trigger\n")
print("=" * 70)

# Download workflow
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)
workflow = response.json()

print(f"📋 Current workflow: {workflow['name']}")
print(f"   Nodes: {len(workflow['nodes'])}")

# Check if cron already exists
if any(n['name'] == 'Morning Summary Trigger' for n in workflow['nodes']):
    print("\n⚠️  Cron trigger already exists!")
    print("   Skipping addition...")
else:
    # Add Cron Trigger Node
    cron_node = {
        "parameters": {
            "rule": {
                "interval": [
                    {
                        "field": "cronExpression",
                        "expression": "30 9 * * 1-5"
                    }
                ]
            }
        },
        "id": "cron-morning",
        "name": "Morning Summary Trigger",
        "type": "n8n-nodes-base.cron",
        "typeVersion": 1.1,
        "position": [240, 200]
    }
    workflow['nodes'].append(cron_node)
    print("\n✅ Added Cron trigger (9:30 AM Mon-Fri)")

    # Add Set Cron Defaults Node
    defaults_node = {
        "parameters": {
            "assignments": {
                "assignments": [
                    {
                        "id": "symbol1-default",
                        "name": "symbol1",
                        "value": "AAPL",
                        "type": "string"
                    },
                    {
                        "id": "symbol2-default",
                        "name": "symbol2",
                        "value": "MSFT",
                        "type": "string"
                    },
                    {
                        "id": "symbol3-default",
                        "name": "symbol3",
                        "value": "PRK",
                        "type": "string"
                    },
                    {
                        "id": "chat-id-default",
                        "name": "chat_id",
                        "value": "1955999067",
                        "type": "string"
                    },
                    {
                        "id": "send-telegram-default",
                        "name": "send_telegram",
                        "value": True,
                        "type": "boolean"
                    }
                ]
            }
        },
        "id": "set-cron-defaults",
        "name": "Set Cron Defaults",
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.3,
        "position": [460, 200]
    }
    workflow['nodes'].append(defaults_node)
    print("✅ Added Set Cron Defaults (AAPL, MSFT, PRK)")

    # Add Merge Triggers Node
    merge_triggers_node = {
        "parameters": {
            "mode": "append",
            "options": {}
        },
        "id": "merge-triggers",
        "name": "Merge Triggers",
        "type": "n8n-nodes-base.merge",
        "typeVersion": 3,
        "position": [680, 300]
    }
    workflow['nodes'].append(merge_triggers_node)
    print("✅ Added Merge Triggers node")

    # Update node positions to accommodate new nodes
    for node in workflow['nodes']:
        if node['name'] == 'Webhook':
            node['position'] = [240, 400]
        elif node['name'] == 'Extract Params':
            node['position'] = [460, 400]
        elif node['name'] == 'Fetch Stock 1':
            node['position'] = [900, 200]
        elif node['name'] == 'Fetch Stock 2':
            node['position'] = [900, 300]
        elif node['name'] == 'Fetch Stock 3':
            node['position'] = [900, 400]

    # Add new connections
    workflow['connections']['Morning Summary Trigger'] = {
        "main": [[{"node": "Set Cron Defaults", "type": "main", "index": 0}]]
    }

    workflow['connections']['Set Cron Defaults'] = {
        "main": [[{"node": "Merge Triggers", "type": "main", "index": 0}]]
    }

    # Update Extract Params to go to Merge Triggers
    workflow['connections']['Extract Params'] = {
        "main": [[{"node": "Merge Triggers", "type": "main", "index": 1}]]
    }

    # Update Merge Triggers to connect to all 3 fetch nodes
    workflow['connections']['Merge Triggers'] = {
        "main": [[
            {"node": "Fetch Stock 1", "type": "main", "index": 0},
            {"node": "Fetch Stock 2", "type": "main", "index": 0},
            {"node": "Fetch Stock 3", "type": "main", "index": 0}
        ]]
    }

    print("✅ Updated all connections")

# Update workflow
workflow_update = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections']
}

# Only include executionOrder from settings if it exists
if 'settings' in workflow and 'executionOrder' in workflow['settings']:
    workflow_update['settings'] = {'executionOrder': workflow['settings']['executionOrder']}

update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json=workflow_update
)

if update_response.status_code == 200:
    print("\n✅ Workflow updated successfully!")
    print("\n📅 Cron Schedule:")
    print("   Time: 9:30 AM")
    print("   Days: Monday - Friday")
    print("   Stocks: AAPL, MSFT, PRK")
    print("   Telegram: Enabled (chat_id: 1955999067)")
    print("\n⏰ Next execution: Check n8n UI for exact time")
    print("\n🧪 Test the webhook (should still work):")
    print('   curl -X POST http://100.82.85.95:5678/webhook/stock-finnhub \\')
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"symbols\": \"GOOGL,AMZN,TSLA\", \"send_to_telegram\": false}'")
else:
    print(f"\n❌ Update failed: {update_response.status_code}")
    print(update_response.text)

print("\n" + "=" * 70)
