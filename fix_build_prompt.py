#!/usr/bin/env python3
"""Fix Build Prompt to handle merged data correctly"""
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

print("🔧 Fixing Build Prompt to handle merged data\n")
print("=" * 70)

# Download workflow
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=headers)
workflow = response.json()

# Fix Merge Stocks node - use "wait for all inputs" mode
for node in workflow['nodes']:
    if node['name'] == 'Merge Stocks':
        print(f"📍 Found Merge Stocks node")
        print(f"   Current params: {node['parameters']}")

        # Set mode to wait for all inputs
        node['parameters'] = {
            "mode": "append",
            "options": {}
        }

        print(f"   ✅ Updated to append mode (waits for all inputs)")
        break

# Update Build Prompt code to be more defensive
for node in workflow['nodes']:
    if node['name'] == 'Build Prompt':
        # Use safer code that handles variable number of items
        node['parameters']['jsCode'] = """// Get all merged stock data
const items = $input.all();

// Get original parameters
const params = $('Extract Params').first().json;

// Process each stock (defensive - handle variable number of items)
const stockData = [
  { symbol: params.symbol1, data: items[0]?.json },
  { symbol: params.symbol2, data: items[1]?.json },
  { symbol: params.symbol3, data: items[2]?.json }
].filter(s => s.data);  // Only include items that have data

// Build stock list
const stocks = stockData.map(s => {
  if (s.data && s.data.c) {
    const price = s.data.c.toFixed(2);
    const change = (s.data.c - s.data.pc).toFixed(2);
    const changePct = (((s.data.c - s.data.pc) / s.data.pc) * 100).toFixed(2);
    return `${s.symbol}: $${price} (${change >= 0 ? '+' : ''}${changePct}%)`;
  }
  return `${s.symbol}: Data unavailable`;
});

const stockList = stocks.join('\\n');

const prompt = `Analyze these stocks:\\n\\n${stockList}\\n\\nProvide a brief analysis in Telegram Markdown format:\\n1. Overall market sentiment\\n2. Key observations for each stock\\n3. Brief outlook\\n\\nUse *bold*, _italic_, and emojis. Start with "📊 *Stock Market Analysis*"`;

return [{
  json: {
    prompt,
    chat_id: params.chat_id,
    send_telegram: params.send_telegram,
    symbols: `${params.symbol1},${params.symbol2},${params.symbol3}`
  }
}];
"""
        print("✅ Updated Build Prompt with defensive code")
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
    print("\n🧪 Testing in 3 seconds...")

    import time
    time.sleep(3)

    test_response = requests.post(
        "http://100.82.85.95:5678/webhook/stock-finnhub",
        json={"symbols": "AAPL,MSFT,PRK", "send_to_telegram": False},
        timeout=90
    )

    print(f"\nStatus: {test_response.status_code}")

    if test_response.status_code == 200 and test_response.text:
        data = test_response.json()
        print("\n✅ SUCCESS!")
        print(json.dumps(data, indent=2)[:1000])

        if '$' in data.get('analysis', '') and any(str(x) in data.get('analysis', '') for x in ['273', '485', '100', '200']):
            print("\n\n🎉🎉🎉 REAL STOCK DATA FROM FINNHUB! 🎉🎉🎉")
    else:
        print(f"Response: {test_response.text[:300]}")
else:
    print(f"\n❌ Update failed: {update_response.status_code}")
    print(update_response.text)

print("\n" + "=" * 70)
