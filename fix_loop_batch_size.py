#!/usr/bin/env python3
"""Fix the Loop Over Symbols node to have proper batchSize"""
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

print("🔧 Fixing Loop Node Configuration\n")
print("=" * 70)

# Download workflow
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID_V3}", headers=headers)
workflow = response.json()

# Find and fix the Loop node
for node in workflow['nodes']:
    if node['name'] == 'Loop Over Symbols' and node['type'] == 'n8n-nodes-base.splitInBatches':
        print(f"📍 Found Loop Over Symbols node")
        print(f"   Current parameters: {node['parameters']}")

        # Add batchSize parameter
        node['parameters']['batchSize'] = 1

        print(f"   ✅ Added batchSize: 1")
        print(f"   New parameters: {node['parameters']}")
        break

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
    print("\n✅ Workflow updated!")
else:
    print(f"\n❌ Update failed: {update_response.status_code}")
    print(update_response.text)
    exit(1)

print("\n" + "=" * 70)
print("🧪 Testing workflow with loop fix...\n")

# Test
test_response = requests.post(
    "http://100.82.85.95:5678/webhook/stock-telegram-v3",
    json={"symbols": "AAPL,MSFT", "send_to_telegram": False},
    timeout=90
)

if test_response.status_code == 200:
    data = test_response.json()
    print("✅ Workflow executed!\n")

    analysis = data.get('analysis', '')

    # Check if we got real data
    if 'unavailable' not in analysis.lower() and 'no price data' not in analysis.lower():
        print("🎉 SUCCESS! Getting real stock data from Finnhub!")
        print(f"\n📊 Analysis preview:")
        print(analysis[:300] + "...")
    else:
        print("⚠️  Still showing no data")
        print(f"\nAnalysis: {analysis[:200]}...")
else:
    print(f"❌ Test failed: {test_response.status_code}")

print("\n" + "=" * 70)
