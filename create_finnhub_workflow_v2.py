#!/usr/bin/env python3
"""Create a new workflow using Finnhub API - properly transformed"""
import json
import requests
import os
from dotenv import load_dotenv
import copy

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
WORKFLOW_ID = os.getenv('WORKFLOW_ID_STOCK_TO_TELEGRAM_V3')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("🚀 Creating Finnhub-based Stock Analysis Workflow\n")
print("=" * 70)

# Download current workflow
print("\n📥 Downloading current workflow...")
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)

if response.status_code != 200:
    print(f"❌ Failed to download: {response.status_code}")
    exit(1)

workflow = response.json()
print(f"✅ Downloaded: {workflow['name']}")

# Create a deep copy for the new workflow
new_workflow = copy.deepcopy(workflow)

# Update workflow metadata
new_workflow['name'] = 'Stock to Telegram v4 (Finnhub)'
print(f"\n📝 New workflow name: {new_workflow['name']}")

# Track changes
changes_log = []

# Process each node
print("\n🔄 Transforming workflow nodes...")

for i, node in enumerate(new_workflow['nodes']):

    # 1. Update Yahoo Finance HTTP Request nodes
    if node['type'] == 'n8n-nodes-base.httpRequest':
        node_str = json.dumps(node.get('parameters', {}))

        if 'finance.yahoo.com' in node_str:
            print(f"\n   📍 Found: {node['name']}")

            # Replace with Finnhub endpoint
            node['parameters'] = {
                'url': '=https://finnhub.io/api/v1/quote?symbol={{ $json.symbol }}&token={{ $credentials.finnhubApi }}',
                'authentication': 'predefinedCredentialType',
                'nodeCredentialType': 'finnhubApi',
                'options': {}
            }

            old_name = node['name']
            node['name'] = old_name.replace('Yahoo Finance', 'Finnhub').replace('Stock Data', 'Stock Quote')

            changes_log.append(f"Updated HTTP node: {old_name} → {node['name']}")
            print(f"   ✅ Converted to Finnhub API")

    # 2. Update data extraction nodes (Set/Edit Fields nodes after stock fetch)
    elif node['type'] == 'n8n-nodes-base.set':
        params = node.get('parameters', {})
        assignments = params.get('assignments', {}).get('assignments', [])

        # Check if this is a stock data extraction node
        has_stock_fields = any(
            a.get('name') in ['symbol', 'price', 'prev_close', 'change']
            for a in assignments
        )

        if has_stock_fields and 'chart.result' in json.dumps(assignments):
            print(f"\n   📍 Found data extraction: {node['name']}")

            # Update assignments for Finnhub response format
            for assignment in assignments:
                if assignment.get('name') == 'symbol':
                    # Symbol stays the same (passed through from previous node)
                    assignment['value'] = '={{ $json.symbol }}'

                elif assignment.get('name') == 'price':
                    # Finnhub uses 'c' for current price
                    assignment['value'] = '={{ $json.c }}'

                elif assignment.get('name') == 'prev_close':
                    # Finnhub uses 'pc' for previous close
                    assignment['value'] = '={{ $json.pc }}'

                elif assignment.get('name') == 'change':
                    # Calculate change from Finnhub data
                    assignment['value'] = '={{ $json.c - $json.pc }}'

                elif assignment.get('name') == 'change_pct':
                    # Calculate percent change
                    assignment['value'] = '={{ (($json.c - $json.pc) / $json.pc) * 100 }}'

            changes_log.append(f"Updated data extraction: {node['name']}")
            print(f"   ✅ Updated for Finnhub response format")

# Update webhook path to avoid conflicts
for node in new_workflow['nodes']:
    if node['type'] == 'n8n-nodes-base.webhook':
        if 'path' in node['parameters']:
            old_path = node['parameters']['path']
            node['parameters']['path'] = 'stock-telegram-v4-finnhub'
            node['webhookId'] = 'stock-telegram-v4-finnhub'
            changes_log.append(f"Updated webhook path: {old_path} → stock-telegram-v4-finnhub")
            print(f"\n   📍 Updated webhook path to avoid conflicts")

print(f"\n✅ Made {len(changes_log)} changes to the workflow")

# Save locally
print("\n💾 Saving new workflow locally...")
with open('finnhub_workflow.json', 'w') as f:
    json.dump(new_workflow, f, indent=2)
print(f"✅ Saved to finnhub_workflow.json")

# Create change log
with open('finnhub_workflow_changes.txt', 'w') as f:
    f.write("Finnhub Workflow Transformation Log\n")
    f.write("=" * 70 + "\n\n")
    for change in changes_log:
        f.write(f"• {change}\n")
print(f"✅ Saved change log to finnhub_workflow_changes.txt")

# Create new workflow in n8n
print("\n" + "=" * 70)
print("🚀 Creating new workflow in n8n...")

workflow_create = {
    'name': new_workflow['name'],
    'nodes': new_workflow['nodes'],
    'connections': new_workflow['connections']
}

if 'settings' in new_workflow:
    allowed_settings = {}
    if 'executionOrder' in new_workflow['settings']:
        allowed_settings['executionOrder'] = new_workflow['settings']['executionOrder']
    if allowed_settings:
        workflow_create['settings'] = allowed_settings

if 'staticData' in new_workflow:
    workflow_create['staticData'] = new_workflow['staticData']

create_response = requests.post(
    f"{N8N_URL}/api/v1/workflows",
    headers=headers,
    json=workflow_create
)

if create_response.status_code in [200, 201]:
    created = create_response.json()
    print(f"✅ New workflow created successfully!")
    print(f"\n📋 Workflow Details:")
    print(f"   ID: {created.get('id')}")
    print(f"   Name: {created.get('name')}")

    # Get the webhook URL
    webhook_url = f"{N8N_URL}/webhook/stock-telegram-v4-finnhub"

    # Save to .env
    env_addition = f"""
# Finnhub Workflow
WORKFLOW_ID_FINNHUB={created.get('id')}
WEBHOOK_URL_FINNHUB={webhook_url}
"""

    with open('.env', 'a') as f:
        f.write(env_addition)

    print(f"\n🌐 Webhook URL: {webhook_url}")

    print(f"\n⚠️  NEXT STEPS:")
    print(f"   1. Sign up for FREE Finnhub API:")
    print(f"      → https://finnhub.io/register")
    print(f"   2. Get your API key:")
    print(f"      → https://finnhub.io/dashboard")
    print(f"   3. Add Finnhub credentials in n8n:")
    print(f"      → {N8N_URL}/credentials")
    print(f"      → Credential type: 'Finnhub API'")
    print(f"      → Name: finnhubApi")
    print(f"      → API Key: <your-key-here>")
    print(f"   4. Activate the workflow in n8n")
    print(f"   5. Test with:")
    print(f"      curl -X POST {webhook_url} \\")
    print(f"        -H 'Content-Type: application/json' \\")
    print(f"        -d '{{\"symbols\": \"AAPL,MSFT\", \"send_to_telegram\": false}}'")

    print(f"\n📚 API Documentation: https://finnhub.io/docs/api")

else:
    print(f"❌ Failed to create workflow: {create_response.status_code}")
    print(f"Response: {create_response.text}")

print("\n" + "=" * 70)
print("\n✨ Summary:")
print(f"   • Transformed {len(changes_log)} components")
print(f"   • Yahoo Finance → Finnhub API")
print(f"   • Free tier: 60 calls/minute")
print(f"   • Real-time stock data")
print(f"   • More reliable than Yahoo Finance")
