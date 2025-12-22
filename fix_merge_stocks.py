#!/usr/bin/env python3
"""Fix workflow by adding Merge node before Build Prompt"""
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

print("🔧 Fixing workflow - adding Merge node\n")
print("=" * 70)

# Download workflow
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)
workflow = response.json()

# Add a Merge node to wait for all 3 stock fetches
merge_stocks_node = {
    "parameters": {
        "mode": "mergeByIndex"
    },
    "id": "merge-stocks",
    "name": "Merge Stocks",
    "type": "n8n-nodes-base.merge",
    "typeVersion": 3,
    "position": [900, 400]
}

# Check if it already exists
if not any(n['name'] == 'Merge Stocks' for n in workflow['nodes']):
    workflow['nodes'].append(merge_stocks_node)
    print("✅ Added Merge Stocks node")

# Update connections
# Change: Fetch Stock 1/2/3 → Build Prompt
# To: Fetch Stock 1/2/3 → Merge Stocks → Build Prompt

workflow['connections']['Fetch Stock 1'] = {
    "main": [[{"node": "Merge Stocks", "type": "main", "index": 0}]]
}
workflow['connections']['Fetch Stock 2'] = {
    "main": [[{"node": "Merge Stocks", "type": "main", "index": 1}]]
}
workflow['connections']['Fetch Stock 3'] = {
    "main": [[{"node": "Merge Stocks", "type": "main", "index": 2}]]
}
workflow['connections']['Merge Stocks'] = {
    "main": [[{"node": "Build Prompt", "type": "main", "index": 0}]]
}

print("✅ Updated connections to use Merge node")

# Move Build Prompt node position
for node in workflow['nodes']:
    if node['name'] == 'Build Prompt':
        node['position'] = [1120, 400]

# Update Build Prompt code to access merged data
for node in workflow['nodes']:
    if node['name'] == 'Build Prompt':
        node['parameters']['jsCode'] = """// Get stock data from merged inputs
const items = $input.all();

// Get symbols from Extract Params
const params = $('Extract Params').first().json;

// Items will be in order: Stock 1, Stock 2, Stock 3
const stock1 = items[0].json;
const stock2 = items[1].json;
const stock3 = items[2].json;

// Build stock list
const stocks = [
  { symbol: params.symbol1, data: stock1 },
  { symbol: params.symbol2, data: stock2 },
  { symbol: params.symbol3, data: stock3 }
];

const stockList = stocks.map(s => {
  if (s.data && s.data.c) {
    const price = s.data.c.toFixed(2);
    const change = (s.data.c - s.data.pc).toFixed(2);
    const changePct = (((s.data.c - s.data.pc) / s.data.pc) * 100).toFixed(2);
    return `${s.symbol}: $${price} (${change >= 0 ? '+' : ''}${changePct}%)`;
  }
  return `${s.symbol}: Data unavailable`;
}).join('\\n');

const prompt = `Analyze these stocks:\\n\\n${stockList}\\n\\nProvide a brief analysis in Telegram Markdown format:\\n1. Overall market sentiment\\n2. Key observations for each stock\\n3. Brief outlook\\n\\nUse *bold*, _italic_, and emojis. Start with "📊 *Stock Market Analysis*"`;

return [{ json: { prompt, chat_id: params.chat_id, send_telegram: params.send_telegram, symbols: `${params.symbol1},${params.symbol2},${params.symbol3}` } }];
"""
        print("✅ Updated Build Prompt to use merged data")
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
    print("\n✅ Workflow updated successfully!")
    print("\n🧪 Test it now:")
    print("   python3 test_final.py")
else:
    print(f"\n❌ Update failed: {update_response.status_code}")
    print(update_response.text)

print("\n" + "=" * 70)
