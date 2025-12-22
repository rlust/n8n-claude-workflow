#!/usr/bin/env python3
"""Fix the prompt to mention Finnhub instead of Yahoo Finance"""
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
WORKFLOW_ID_V3 = os.getenv('WORKFLOW_ID_STOCK_TO_TELEGRAM_V3')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("🔧 Fixing Prompt References\n")
print("=" * 70)

# Download workflow
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID_V3}", headers=headers)
workflow = response.json()

# Find and update Build Prompt node
for node in workflow['nodes']:
    if node['name'] == 'Build Prompt' and node['type'] == 'n8n-nodes-base.code':
        print(f"📍 Found Build Prompt node")

        code = node['parameters'].get('jsCode', '')

        # Replace Yahoo Finance references
        updated_code = code.replace(
            'no price data was available from Yahoo Finance',
            'no price data was available from Finnhub API'
        ).replace(
            'Yahoo Finance',
            'Finnhub'
        )

        if updated_code != code:
            node['parameters']['jsCode'] = updated_code
            print("   ✅ Updated Yahoo Finance → Finnhub")
        else:
            print("   ⚠️  No changes needed")

# Update workflow
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
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID_V3}",
    headers=headers,
    json=workflow_update
)

if update_response.status_code == 200:
    print("✅ Workflow updated!\n")
else:
    print(f"❌ Update failed: {update_response.status_code}\n")

print("=" * 70)
print("🧪 Testing workflow...\n")

# Test the workflow
test_response = requests.post(
    "http://100.82.85.95:5678/webhook/stock-telegram-v3",
    json={"symbols": "AAPL", "send_to_telegram": False},
    timeout=60
)

if test_response.status_code == 200:
    data = test_response.json()
    print("✅ Workflow executed!")
    print(f"\nResponse:")
    print(json.dumps(data, indent=2))

    analysis = data.get('analysis', '')
    if 'unavailable' in analysis.lower() or 'no price data' in analysis.lower():
        print("\n⚠️  Still showing no price data")
        print("   This might be a deeper issue with the HTTP node configuration")
    else:
        print("\n🎉 SUCCESS! Getting real stock data from Finnhub!")
else:
    print(f"❌ Test failed: {test_response.status_code}")
    print(test_response.text[:500])

print("\n" + "=" * 70)
