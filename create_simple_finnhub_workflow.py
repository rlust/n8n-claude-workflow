#!/usr/bin/env python3
"""Create a simple, working Finnhub workflow without loops"""
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

print("🚀 Creating Simple Finnhub Workflow (No Loops!)\n")
print("=" * 70)

# Create a simple workflow
workflow = {
    "name": "Stock to Telegram v5 (Simple Finnhub)",
    "nodes": [
        # Webhook trigger
        {
            "parameters": {
                "httpMethod": "POST",
                "path": "stock-telegram-v5",
                "responseMode": "responseNode",
                "options": {}
            },
            "id": "webhook",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [240, 300],
            "webhookId": "stock-telegram-v5"
        },

        # Code node to fetch stocks and build prompt
        {
            "parameters": {
                "jsCode": f"""// Get symbols from webhook
const symbolsInput = $json.body.symbols || 'AAPL,MSFT,PRK';
const symbols = symbolsInput.split(',').map(s => s.trim()).filter(Boolean);
const chatId = $json.body.chat_id || '1955999067';
const sendTelegram = $json.body.send_to_telegram !== false;

// Fetch stock data from Finnhub
const stockData = [];

for (const symbol of symbols) {{
  try {{
    const response = await fetch(
      `https://finnhub.io/api/v1/quote?symbol=${{symbol}}&token={FINNHUB_API_KEY}`
    );
    const data = await response.json();

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
            },
            "id": "fetch-and-build",
            "name": "Fetch Stocks & Build Prompt",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [460, 300]
        },

        # Call Claude
        {
            "parameters": {
                "method": "POST",
                "url": "https://api.anthropic.com/v1/messages",
                "authentication": "predefinedCredentialType",
                "nodeCredentialType": "anthropicApi",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {"name": "anthropic-version", "value": "2023-06-01"}
                    ]
                },
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": '={{ {"model": "claude-sonnet-4-5-20250929", "max_tokens": 1024, "messages": [{"role": "user", "content": $json.prompt}]} }}',
                "options": {}
            },
            "id": "call-claude",
            "name": "Call Claude",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [680, 300],
            "credentials": {
                "anthropicApi": {
                    "id": "REYgTvbzUh2zQgDS",
                    "name": "x-api-key"
                }
            }
        },

        # Extract response
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {
                            "id": "analysis",
                            "name": "analysis",
                            "value": "={{ $json.content[0].text }}",
                            "type": "string"
                        },
                        {
                            "id": "tokens",
                            "name": "tokens",
                            "value": "={{ $json.usage.input_tokens + $json.usage.output_tokens }}",
                            "type": "number"
                        },
                        {
                            "id": "chat_id",
                            "name": "chat_id",
                            "value": "={{ $('Fetch Stocks & Build Prompt').item.json.chatId }}",
                            "type": "string"
                        },
                        {
                            "id": "send_telegram",
                            "name": "send_telegram",
                            "value": "={{ $('Fetch Stocks & Build Prompt').item.json.sendTelegram }}",
                            "type": "boolean"
                        },
                        {
                            "id": "symbols",
                            "name": "symbols",
                            "value": "={{ $('Fetch Stocks & Build Prompt').item.json.symbols }}",
                            "type": "string"
                        }
                    ]
                }
            },
            "id": "extract",
            "name": "Extract Response",
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.3,
            "position": [900, 300]
        },

        # If - Send Telegram?
        {
            "parameters": {
                "conditions": {
                    "boolean": [
                        {"value1": "={{ $json.send_telegram }}", "value2": True}
                    ]
                }
            },
            "id": "if-telegram",
            "name": "Send Telegram?",
            "type": "n8n-nodes-base.if",
            "typeVersion": 1,
            "position": [1120, 300]
        },

        # Send to Telegram
        {
            "parameters": {
                "chatId": "={{ $json.chat_id }}",
                "text": "={{ $json.analysis }}",
                "additionalFields": {
                    "disable_web_page_preview": True,
                    "parse_mode": "Markdown"
                }
            },
            "id": "telegram",
            "name": "Send to Telegram",
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [1340, 200],
            "credentials": {
                "telegramApi": {
                    "id": "RU8X7kcB4vm0KAFx",
                    "name": "Telegram API"
                }
            }
        },

        # Telegram Response
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {"id": "telegram_sent", "name": "telegram_sent", "value": True, "type": "boolean"},
                        {"id": "telegram_id", "name": "telegram_message_id", "value": "={{ $json.result.message_id }}", "type": "number"}
                    ]
                }
            },
            "id": "telegram-response",
            "name": "Telegram Response",
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.3,
            "position": [1560, 200]
        },

        # No Telegram Response
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {"id": "telegram_sent", "name": "telegram_sent", "value": False, "type": "boolean"}
                    ]
                }
            },
            "id": "no-telegram",
            "name": "No Telegram",
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.3,
            "position": [1340, 400]
        },

        # Merge
        {
            "parameters": {},
            "id": "merge",
            "name": "Merge",
            "type": "n8n-nodes-base.merge",
            "typeVersion": 3,
            "position": [1780, 300]
        },

        # Respond
        {
            "parameters": {
                "respondWith": "json",
                "responseBody": '={{ {"success": true, "symbols": $("Extract Response").item.json.symbols, "analysis": $("Extract Response").item.json.analysis, "tokens_used": $("Extract Response").item.json.tokens, "telegram_sent": $json.telegram_sent, "telegram_message_id": $json.telegram_message_id || null} }}',
                "options": {}
            },
            "id": "respond",
            "name": "Respond",
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.1,
            "position": [2000, 300]
        }
    ],
    "connections": {
        "Webhook": {"main": [[{"node": "Fetch Stocks & Build Prompt", "type": "main", "index": 0}]]},
        "Fetch Stocks & Build Prompt": {"main": [[{"node": "Call Claude", "type": "main", "index": 0}]]},
        "Call Claude": {"main": [[{"node": "Extract Response", "type": "main", "index": 0}]]},
        "Extract Response": {"main": [[{"node": "Send Telegram?", "type": "main", "index": 0}]]},
        "Send Telegram?": {
            "main": [
                [{"node": "Send to Telegram", "type": "main", "index": 0}],
                [{"node": "No Telegram", "type": "main", "index": 0}]
            ]
        },
        "Send to Telegram": {"main": [[{"node": "Telegram Response", "type": "main", "index": 0}]]},
        "Telegram Response": {"main": [[{"node": "Merge", "type": "main", "index": 0}]]},
        "No Telegram": {"main": [[{"node": "Merge", "type": "main", "index": 1}]]},
        "Merge": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]}
    },
    "settings": {
        "executionOrder": "v1"
    }
}

print("📝 Creating workflow in n8n...")

create_response = requests.post(
    f"{N8N_URL}/api/v1/workflows",
    headers=headers,
    json=workflow
)

if create_response.status_code in [200, 201]:
    created = create_response.json()
    workflow_id = created.get('id')

    print(f"✅ Workflow created!")
    print(f"\n📋 Details:")
    print(f"   ID: {workflow_id}")
    print(f"   Name: {created.get('name')}")
    print(f"   Webhook: http://100.82.85.95:5678/webhook/stock-telegram-v5")

    # Activate it
    print(f"\n⚡ Activating workflow...")
    activate_response = requests.patch(
        f"{N8N_URL}/api/v1/workflows/{workflow_id}",
        headers=headers,
        json={'active': True}
    )

    if activate_response.status_code == 200:
        print(f"   ✅ Activated!")

    # Save to .env
    with open('.env', 'a') as f:
        f.write(f"\nWORKFLOW_ID_V5_SIMPLE={workflow_id}\n")
        f.write(f"WEBHOOK_URL_V5_SIMPLE=http://100.82.85.95:5678/webhook/stock-telegram-v5\n")

    print(f"\n" + "=" * 70)
    print(f"🧪 Testing the new simple workflow...")
    print(f"=" * 70 + "\n")

    import time
    time.sleep(2)

    test_response = requests.post(
        "http://100.82.85.95:5678/webhook/stock-telegram-v5",
        json={"symbols": "AAPL,MSFT", "send_to_telegram": False},
        timeout=60
    )

    if test_response.status_code == 200:
        data = test_response.json()
        print("✅ Test successful!\n")
        print(json.dumps(data, indent=2)[:800])

        if 'AAPL' in data.get('analysis', '') and '$' in data.get('analysis', ''):
            print("\n\n🎉🎉🎉 SUCCESS! Real stock data from Finnhub! 🎉🎉🎉")
        else:
            print("\n⚠️  Check the analysis above")
    else:
        print(f"❌ Test failed: {test_response.status_code}")
        print(test_response.text[:500])

else:
    print(f"❌ Failed to create: {create_response.status_code}")
    print(create_response.text)

print("\n" + "=" * 70)
