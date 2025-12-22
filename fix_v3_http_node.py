#!/usr/bin/env python3
"""Fix the v3 HTTP Request node configuration"""
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
WORKFLOW_ID_V3 = os.getenv('WORKFLOW_ID_STOCK_TO_TELEGRAM_V3')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("🔧 Fixing v3 HTTP Request Node\n")
print("=" * 70)

# Download workflow
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID_V3}", headers=headers)
workflow = response.json()

# Find and fix the Finnhub HTTP node
for node in workflow['nodes']:
    if node['name'] == 'Fetch Stock Data' and node['type'] == 'n8n-nodes-base.httpRequest':
        print("📍 Found Fetch Stock Data node")
        print(f"   Current params: {node['parameters']}")

        # Set proper HTTP Request configuration
        node['parameters'] = {
            'method': 'GET',  # Explicitly set GET method
            'url': f'=https://finnhub.io/api/v1/quote?symbol={{{{ $json.symbol }}}}&token={FINNHUB_API_KEY}',
            'options': {
                'response': {
                    'response': {
                        'responseFormat': 'json'
                    }
                }
            }
        }

        print(f"\n   ✅ Updated configuration:")
        print(f"      Method: GET")
        print(f"      URL: ...finnhub.io/api/v1/quote...")
        print(f"      Response format: JSON")
        break

# Update workflow
workflow_update = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections']
}

# Only add allowed settings fields
if 'settings' in workflow and 'executionOrder' in workflow['settings']:
    workflow_update['settings'] = {'executionOrder': workflow['settings']['executionOrder']}

update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID_V3}",
    headers=headers,
    json=workflow_update
)

if update_response.status_code == 200:
    print("\n✅ Workflow updated!")
else:
    print(f"\n❌ Update failed: {update_response.status_code}")
    print(update_response.text)
    exit(1)

print("\n" + "=" * 70)
print("📋 Now test the 'Fetch Stock Data' node in n8n:")
print("   1. Open the v3 workflow")
print("   2. Click 'Loop Over Symbols' node")
print("   3. Click 'Test step'")
print("   4. Then click 'Fetch Stock Data' node")
print("   5. Click 'Test step' again")
print("   6. You should see Finnhub data!")
print("=" * 70)
