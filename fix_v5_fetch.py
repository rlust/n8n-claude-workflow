#!/usr/bin/env python3
"""Fix v5 workflow to use n8n's $http instead of fetch"""
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
WORKFLOW_ID_V5 = os.getenv('WORKFLOW_ID_V5_SIMPLE')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("🔧 Fixing v5 workflow to use n8n's HTTP method\n")
print("=" * 70)

# Download workflow
response = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID_V5}", headers=headers)
workflow = response.json()

# Find and fix the code node
for node in workflow['nodes']:
    if node['name'] == 'Fetch Stocks & Build Prompt':
        print("📍 Found code node")

        # Replace with n8n-compatible code
        node['parameters']['jsCode'] = f"""// Get symbols from webhook
const symbolsInput = $json.body.symbols || 'AAPL,MSFT,PRK';
const symbols = symbolsInput.split(',').map(s => s.trim()).filter(Boolean);
const chatId = $json.body.chat_id || '1955999067';
const sendTelegram = $json.body.send_to_telegram !== false;

// Fetch stock data from Finnhub using n8n's $http
const stockData = [];

for (const symbol of symbols) {{
  try {{
    const response = await $http.request({{
      method: 'GET',
      url: `https://finnhub.io/api/v1/quote?symbol=${{symbol}}&token={FINNHUB_API_KEY}`,
      json: true
    }});

    const data = response;

    if (data.c) {{
      const price = data.c.toFixed(2);
      const prevClose = data.pc.toFixed(2);
      const change = (data.c - data.pc).toFixed(2);
      const changePct = (((data.c - data.pc) / data.pc) * 100).toFixed(2);

      stockData.push({{
        symbol,
        price,
        change,
        changePct,
        display: `${{symbol}}: $${{price}} (${{change >= 0 ? '+' : ''}}${{changePct}}%)`
      }});
    }} else {{
      stockData.push({{
        symbol,
        display: `${{symbol}}: Data unavailable`
      }});
    }}
  }} catch (error) {{
    stockData.push({{
      symbol,
      display: `${{symbol}}: Error - ${{error.message}}`
    }});
  }}
}}

// Build prompt
const stockList = stockData.map(s => s.display).join('\\\\n');

const prompt = stockData.some(s => s.price)
  ? `Analyze these stocks:\\\\n\\\\n${{stockList}}\\\\n\\\\nProvide a brief analysis in Telegram Markdown format:\\\\n1. Overall market sentiment\\\\n2. Key observations for each stock\\\\n3. Brief outlook\\\\n\\\\nUse *bold*, _italic_, and emojis. Start with "📊 *Stock Market Analysis*"`
  : `These stocks were requested but data is unavailable:\\\\n\\\\n${{stockList}}\\\\n\\\\nProvide a brief explanation and recommendations in Telegram Markdown format. Use *bold*, _italic_, and emojis.`;

return [{{
  json: {{
    prompt,
    chatId,
    sendTelegram,
    symbols: symbolsInput,
    stockData
  }}
}}];
"""

        print("✅ Updated to use $http.request()")
        break

# Update workflow
workflow_update = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections'],
    'settings': workflow.get('settings', {'executionOrder': 'v1'})
}

update_response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID_V5}",
    headers=headers,
    json=workflow_update
)

if update_response.status_code == 200:
    print("✅ Workflow updated!\n")
else:
    print(f"❌ Update failed: {update_response.status_code}")
    print(update_response.text)
    exit(1)

print("=" * 70)
print("🧪 Testing updated workflow...\n")

import time
time.sleep(2)

test_response = requests.post(
    "http://100.82.85.95:5678/webhook/stock-telegram-v5",
    json={"symbols": "AAPL,MSFT,PRK", "send_to_telegram": False},
    timeout=60
)

if test_response.status_code == 200:
    data = test_response.json()
    print("✅ Workflow executed!\n")

    analysis = data.get('analysis', '')

    # Check for real stock data
    if '$' in analysis and any(x in analysis for x in ['273', '485', '100', '200', '300']):
        print("🎉🎉🎉 SUCCESS! Real stock prices from Finnhub! 🎉🎉🎉\n")
        print(analysis[:500])
    elif 'error' in analysis.lower() or 'unavailable' in analysis.lower():
        print("⚠️  Still having issues:\n")
        print(analysis[:400])
    else:
        print("📊 Response:\n")
        print(analysis[:400])
else:
    print(f"❌ Test failed: {test_response.status_code}")

print("\n" + "=" * 70)
