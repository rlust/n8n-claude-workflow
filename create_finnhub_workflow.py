#!/usr/bin/env python3
"""Create a new workflow using Finnhub API instead of Yahoo Finance"""
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

# Find and update the stock fetch nodes
print("\n🔄 Converting Yahoo Finance nodes to Finnhub...")

nodes_updated = []

for node in new_workflow['nodes']:
    # Find the Yahoo Finance HTTP Request nodes
    if node['type'] == 'n8n-nodes-base.httpRequest' and 'finance.yahoo.com' in json.dumps(node):
        print(f"\n   📍 Found Yahoo Finance node: {node['name']}")

        # Update to Finnhub API
        node['parameters'] = {
            'url': '=https://finnhub.io/api/v1/quote?symbol={{ $json.symbol }}&token={{ $credentials.finnhubApi.apiKey }}',
            'authentication': 'predefinedCredentialType',
            'nodeCredentialType': 'finnhubApi',
            'options': {}
        }

        # Update node name
        old_name = node['name']
        node['name'] = old_name.replace('Yahoo Finance', 'Finnhub')

        nodes_updated.append(old_name)
        print(f"   ✅ Updated to Finnhub API")

    # Update Build Prompt node to handle Finnhub response format
    elif node['name'] == 'Build Prompt':
        print(f"\n   📍 Updating Build Prompt for Finnhub response format...")

        # Finnhub returns: {c: current_price, h: high, l: low, o: open, pc: previous_close, t: timestamp}
        # We need to update the prompt building logic

        params = node['parameters']
        if 'value' in params:
            # Update the prompt template to use Finnhub data structure
            old_prompt = params['value']

            # Replace Yahoo Finance data references with Finnhub
            # Yahoo: price, previousClose, etc
            # Finnhub: c (current), pc (previous close), h (high), l (low), o (open)

            new_prompt = old_prompt.replace(
                '$json.price',
                '$json.c'  # current price in Finnhub
            ).replace(
                '$json.previousClose',
                '$json.pc'  # previous close in Finnhub
            ).replace(
                '$json.regularMarketPrice',
                '$json.c'
            ).replace(
                '$json.regularMarketPreviousClose',
                '$json.pc'
            )

            params['value'] = new_prompt
            print(f"   ✅ Updated prompt template for Finnhub data structure")

print(f"\n✅ Updated {len(nodes_updated)} nodes")

# Save locally first
print("\n💾 Saving new workflow locally...")
with open('finnhub_workflow.json', 'w') as f:
    json.dump(new_workflow, f, indent=2)
print(f"✅ Saved to finnhub_workflow.json")

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

    # Save the workflow ID
    with open('.env', 'a') as f:
        f.write(f"\nWORKFLOW_ID_FINNHUB={created.get('id')}")

    print(f"\n⚠️  IMPORTANT: You need to:")
    print(f"   1. Sign up for free Finnhub API at: https://finnhub.io/register")
    print(f"   2. Get your API key from: https://finnhub.io/dashboard")
    print(f"   3. Add Finnhub credentials in n8n at:")
    print(f"      {N8N_URL}/credentials")
    print(f"   4. Set credential type: 'Finnhub API'")
    print(f"   5. Activate the workflow")

else:
    print(f"❌ Failed to create workflow: {create_response.status_code}")
    print(f"Response: {create_response.text}")

print("\n" + "=" * 70)
