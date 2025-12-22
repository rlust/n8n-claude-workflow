#!/usr/bin/env python3
"""Create ultra-simple test workflow - just fetch AAPL price"""
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("🚀 Creating Ultra-Simple Test Workflow\n")
print("=" * 70)

workflow = {
    "name": "Finnhub Test (Simple)",
    "nodes": [
        {
            "parameters": {
                "httpMethod": "POST",
                "path": "finnhub-test",
                "responseMode": "responseNode",
                "options": {}
            },
            "id": "webhook",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [240, 300],
            "webhookId": "finnhub-test"
        },
        {
            "parameters": {
                "method": "GET",
                "url": f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={FINNHUB_API_KEY}",
                "options": {}
            },
            "id": "http",
            "name": "Fetch AAPL from Finnhub",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [460, 300]
        },
        {
            "parameters": {
                "respondWith": "json",
                "responseBody": "={{ $json }}",
                "options": {}
            },
            "id": "respond",
            "name": "Respond",
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.1,
            "position": [680, 300]
        }
    ],
    "connections": {
        "Webhook": {"main": [[{"node": "Fetch AAPL from Finnhub", "type": "main", "index": 0}]]},
        "Fetch AAPL from Finnhub": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]}
    },
    "settings": {
        "executionOrder": "v1"
    }
}

print("📝 Creating test workflow...")

create_response = requests.post(
    f"{N8N_URL}/api/v1/workflows",
    headers=headers,
    json=workflow
)

if create_response.status_code in [200, 201]:
    created = create_response.json()
    workflow_id = created.get('id')

    print(f"✅ Created: {created.get('name')}")
    print(f"   ID: {workflow_id}")
    print(f"   Webhook: http://100.82.85.95:5678/webhook/finnhub-test")

    # Activate
    print(f"\n⚡ Activating...")
    requests.patch(f"{N8N_URL}/api/v1/workflows/{workflow_id}", headers=headers, json={'active': True})

    print("\n" + "=" * 70)
    print("✅ Workflow created and activated!")
    print("=" * 70)
    print("\n🧪 Test it:")
    print("   curl -X POST http://100.82.85.95:5678/webhook/finnhub-test")
    print("\nYou should see:")
    print('   {"c": 273.67, "h": 274.6, "l": 269.9, ...}')
    print("\n" + "=" * 70)

else:
    print(f"❌ Failed: {create_response.status_code}")
    print(create_response.text)
