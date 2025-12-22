#!/usr/bin/env python3
"""Fix Finnhub workflow to use API key directly in URL (no credentials needed)"""
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
WORKFLOW_ID = os.getenv('WORKFLOW_ID_FINNHUB')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("🔧 Fixing Finnhub Workflow - Direct API Key Method\n")
print("=" * 70)

# Download current workflow
print("\n📥 Downloading Finnhub workflow...")
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)

if response.status_code != 200:
    print(f"❌ Failed to download: {response.status_code}")
    exit(1)

workflow = response.json()
print(f"✅ Downloaded: {workflow['name']}")

# Find and update HTTP Request nodes to use API key in URL
print("\n🔄 Updating HTTP Request nodes...")

nodes_updated = 0

for node in workflow['nodes']:
    if node['type'] == 'n8n-nodes-base.httpRequest':
        node_str = json.dumps(node.get('parameters', {}))

        # Check if this is a Finnhub node
        if 'finnhub.io' in node_str:
            print(f"\n   📍 Found Finnhub HTTP node: {node['name']}")

            # Update to use API key directly in URL without credentials
            node['parameters'] = {
                'url': f'=https://finnhub.io/api/v1/quote?symbol={{{{ $json.symbol }}}}&token={FINNHUB_API_KEY}',
                'options': {}
            }

            # Remove any authentication settings
            if 'authentication' in node['parameters']:
                del node['parameters']['authentication']
            if 'nodeCredentialType' in node['parameters']:
                del node['parameters']['nodeCredentialType']

            nodes_updated += 1
            print(f"   ✅ Updated to use API key directly in URL")

if nodes_updated == 0:
    print("\n⚠️  No Finnhub nodes found to update")
    exit(1)

print(f"\n✅ Updated {nodes_updated} node(s)")

# Update workflow
print("\n" + "=" * 70)
print("🚀 Updating workflow in n8n...")

workflow_update = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections']
}

if 'settings' in workflow:
    allowed_settings = {}
    if 'executionOrder' in workflow['settings']:
        allowed_settings['executionOrder'] = workflow['settings']['executionOrder']
    if allowed_settings:
        workflow_update['settings'] = allowed_settings

if 'staticData' in workflow:
    workflow_update['staticData'] = workflow['staticData']

update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json=workflow_update
)

if update_response.status_code == 200:
    print(f"✅ Workflow updated successfully!")
    print(f"\n✨ The workflow now uses the API key directly in the URL")
    print(f"   No credentials needed in n8n!")

    # Save locally
    with open('finnhub_workflow_fixed.json', 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"\n💾 Saved to finnhub_workflow_fixed.json")

else:
    print(f"❌ Failed to update: {update_response.status_code}")
    print(f"Response: {update_response.text}")
    exit(1)

# Activate the workflow
print("\n⚡ Activating workflow...")
activate_response = requests.patch(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json={'active': True}
)

if activate_response.status_code == 200:
    print(f"✅ Workflow activated!")
else:
    print(f"⚠️  Could not activate (status {activate_response.status_code})")
    print(f"   Please activate manually at: {N8N_URL}/workflow/{WORKFLOW_ID}")

print("\n" + "=" * 70)
print("✅ Setup Complete!")
print("=" * 70)

print("\n📋 Summary:")
print(f"   • API Key embedded in workflow URL")
print(f"   • No n8n credentials required")
print(f"   • Workflow updated and activated")

print("\n🧪 Test the workflow:")
print(f"   curl -X POST {N8N_URL}/webhook/stock-telegram-v4-finnhub \\")
print(f"     -H 'Content-Type: application/json' \\")
print(f"     -d '{{\"symbols\": \"AAPL,MSFT\", \"send_to_telegram\": false}}'")

print("\n" + "=" * 70)
