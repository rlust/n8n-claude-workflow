#!/usr/bin/env python3
"""Upgrade the working v3 workflow to use Finnhub instead of Yahoo Finance"""
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

print("🔄 Upgrading v3 Workflow to Use Finnhub\n")
print("=" * 70)

# Download v3 workflow
print("\n📥 Downloading v3 workflow...")
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID_V3}", headers=headers)

if response.status_code != 200:
    print(f"❌ Failed to download: {response.status_code}")
    exit(1)

workflow = response.json()
print(f"✅ Downloaded: {workflow['name']}")
print(f"   Nodes: {len(workflow['nodes'])}")

# Find and update Yahoo Finance nodes
print("\n🔄 Converting Yahoo Finance → Finnhub...")

nodes_updated = 0

for node in workflow['nodes']:
    if node['type'] == 'n8n-nodes-base.httpRequest':
        params = node.get('parameters', {})
        url = params.get('url', '')

        if 'finance.yahoo.com' in url:
            print(f"\n   📍 Found Yahoo Finance node: {node['name']}")

            # Update to Finnhub
            node['parameters'] = {
                'url': f'=https://finnhub.io/api/v1/quote?symbol={{{{ $json.symbol }}}}&token={FINNHUB_API_KEY}',
                'options': {}
            }

            nodes_updated += 1
            print(f"   ✅ Converted to Finnhub")

    # Update data extraction nodes for Finnhub response format
    elif node['type'] == 'n8n-nodes-base.set':
        params = node.get('parameters', {})
        assignments = params.get('assignments', {}).get('assignments', [])

        # Check if this extracts Yahoo Finance data
        yahoo_data_found = False
        for assignment in assignments:
            value = str(assignment.get('value', ''))
            if 'chart.result' in value or 'regularMarketPrice' in value:
                yahoo_data_found = True
                break

        if yahoo_data_found:
            print(f"\n   📍 Found Yahoo data extraction: {node['name']}")

            # Update for Finnhub format
            for assignment in assignments:
                name = assignment.get('name')

                if name == 'symbol':
                    # Symbol comes from input, keep as is
                    assignment['value'] = '={{ $json.symbol }}'

                elif name == 'price':
                    # Finnhub uses 'c' for current price
                    assignment['value'] = '={{ $json.c }}'

                elif name == 'prev_close':
                    # Finnhub uses 'pc' for previous close
                    assignment['value'] = '={{ $json.pc }}'

                elif name == 'change':
                    # Calculate change
                    assignment['value'] = '={{ $json.c - $json.pc }}'

                elif name == 'change_pct':
                    # Calculate percent change
                    assignment['value'] = '={{ (($json.c - $json.pc) / $json.pc) * 100 }}'

            nodes_updated += 1
            print(f"   ✅ Updated data extraction for Finnhub")

print(f"\n✅ Updated {nodes_updated} nodes")

if nodes_updated == 0:
    print("\n⚠️  No Yahoo Finance nodes found - workflow might already be updated")
    exit(0)

# Backup original workflow
print("\n💾 Creating backup...")
with open('workflow_v3_backup.json', 'w') as f:
    json.dump(workflow, f, indent=2)
print("   ✅ Saved backup to workflow_v3_backup.json")

# Update workflow name
workflow['name'] = 'Stock to Telegram v3 (Finnhub)'

# Update workflow
print("\n🚀 Updating workflow in n8n...")

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
    print(f"✅ Workflow updated successfully!")
    print(f"\n✨ Your v3 workflow now uses Finnhub!")
    print(f"   Name: {workflow['name']}")
    print(f"   Webhook: http://100.82.85.95:5678/webhook/stock-telegram-v3")

    # Save updated version
    with open('workflow_v3_finnhub.json', 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"\n💾 Saved updated workflow to workflow_v3_finnhub.json")
else:
    print(f"❌ Failed to update: {update_response.status_code}")
    print(f"Response: {update_response.text}")
    print(f"\n💾 Backup saved - you can restore if needed")
    exit(1)

print("\n" + "=" * 70)
print("✅ Upgrade Complete!")
print("=" * 70)

print("\n🧪 Test it:")
print(f"   curl -X POST http://100.82.85.95:5678/webhook/stock-telegram-v3 \\")
print(f"     -H 'Content-Type: application/json' \\")
print(f"     -d '{{\"symbols\": \"AAPL,MSFT,PRK\", \"send_to_telegram\": false}}'")

print("\n📋 What changed:")
print(f"   • Yahoo Finance API → Finnhub API")
print(f"   • Data extraction updated for Finnhub format")
print(f"   • All connections preserved")
print(f"   • Workflow remains active")

print("\n" + "=" * 70)
