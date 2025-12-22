#!/usr/bin/env python3
"""Fix Merge node configuration"""
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

print("🔧 Fixing Merge node configuration\n")
print("=" * 70)

# Download workflow
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)
workflow = response.json()

# Fix Merge Stocks node
for node in workflow['nodes']:
    if node['name'] == 'Merge Stocks':
        print(f"📍 Found Merge Stocks node")
        print(f"   Current params: {node['parameters']}")

        # Use simpler configuration
        node['parameters'] = {}

        print(f"   ✅ Updated to default merge mode")
        break

# Update workflow
workflow_update = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections']
}

if 'settings' in workflow and 'executionOrder' in workflow['settings']:
    workflow_update['settings'] = {'executionOrder': workflow['settings']['executionOrder']}

update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json=workflow_update
)

if update_response.status_code == 200:
    print("\n✅ Workflow updated!")
    print("\n🧪 Testing...")

    import time
    time.sleep(2)

    test_response = requests.post(
        "http://100.82.85.95:5678/webhook/stock-finnhub",
        json={"symbols": "AAPL,MSFT,PRK", "send_to_telegram": False},
        timeout=90
    )

    print(f"\nStatus: {test_response.status_code}")

    if test_response.status_code == 200 and test_response.text:
        data = test_response.json()
        print("\n✅ SUCCESS!")
        print(json.dumps(data, indent=2)[:800])

        if '$' in data.get('analysis', '') and any(str(x) in data.get('analysis', '') for x in ['273', '485', '100', '200']):
            print("\n\n🎉🎉🎉 REAL STOCK DATA FROM FINNHUB! 🎉🎉🎉")
    else:
        print(f"Response: {test_response.text[:200]}")
else:
    print(f"\n❌ Update failed: {update_response.status_code}")
    print(update_response.text)

print("\n" + "=" * 70)
