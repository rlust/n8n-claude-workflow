#!/usr/bin/env python3
"""Create complete working Finnhub workflow with parallel stock fetching"""
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

print("🚀 Creating Complete Working Finnhub Workflow\n")
print("=" * 70)

workflow = {
    "name": "Stock to Telegram (Finnhub Working)",
    "nodes": [
        # Webhook
        {
            "parameters": {"httpMethod": "POST", "path": "stock-finnhub", "responseMode": "responseNode", "options": {}},
            "id": "webhook", "name": "Webhook", "type": "n8n-nodes-base.webhook", "typeVersion": 2,
            "position": [240, 400], "webhookId": "stock-finnhub"
        },

        # Extract params
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {"id": "s1", "name": "symbol1", "value": "={{ $json.body.symbols ? $json.body.symbols.split(',')[0]?.trim() || 'AAPL' : 'AAPL' }}", "type": "string"},
                        {"id": "s2", "name": "symbol2", "value": "={{ $json.body.symbols ? $json.body.symbols.split(',')[1]?.trim() || 'MSFT' : 'MSFT' }}", "type": "string"},
                        {"id": "s3", "name": "symbol3", "value": "={{ $json.body.symbols ? $json.body.symbols.split(',')[2]?.trim() || 'PRK' : 'PRK' }}", "type": "string"},
                        {"id": "chat", "name": "chat_id", "value": "={{ $json.body.chat_id || '1955999067' }}", "type": "string"},
                        {"id": "tg", "name": "send_telegram", "value": "={{ $json.body.send_to_telegram !== false }}", "type": "boolean"}
                    ]
                }
            },
            "id": "extract", "name": "Extract Params", "type": "n8n-nodes-base.set", "typeVersion": 3.3,
            "position": [460, 400]
        },

        # Fetch Stock 1
        {
            "parameters": {
                "method": "GET",
                "url": f"=https://finnhub.io/api/v1/quote?symbol={{{{ $json.symbol1 }}}}&token={FINNHUB_API_KEY}",
                "options": {}
            },
            "id": "http1", "name": "Fetch Stock 1", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2,
            "position": [680, 200]
        },

        # Fetch Stock 2
        {
            "parameters": {
                "method": "GET",
                "url": f"=https://finnhub.io/api/v1/quote?symbol={{{{ $json.symbol2 }}}}&token={FINNHUB_API_KEY}",
                "options": {}
            },
            "id": "http2", "name": "Fetch Stock 2", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2,
            "position": [680, 400]
        },

        # Fetch Stock 3
        {
            "parameters": {
                "method": "GET",
                "url": f"=https://finnhub.io/api/v1/quote?symbol={{{{ $json.symbol3 }}}}&token={FINNHUB_API_KEY}",
                "options": {}
            },
            "id": "http3", "name": "Fetch Stock 3", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2,
            "position": [680, 600]
        },

        # Build Prompt
        {
            "parameters": {
                "jsCode": """// Get stock data from all three fetches
const stock1 = $('Fetch Stock 1').first().json;
const stock2 = $('Fetch Stock 2').first().json;
const stock3 = $('Fetch Stock 3').first().json;

// Get symbols from Extract Params
const params = $('Extract Params').first().json;

// Build stock list
const stocks = [
  { symbol: params.symbol1, data: stock1 },
  { symbol: params.symbol2, data: stock2 },
  { symbol: params.symbol3, data: stock3 }
];

const stockList = stocks.map(s => {
  if (s.data.c) {
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
            },
            "id": "build", "name": "Build Prompt", "type": "n8n-nodes-base.code", "typeVersion": 2,
            "position": [900, 400]
        },

        # Call Claude
        {
            "parameters": {
                "method": "POST", "url": "https://api.anthropic.com/v1/messages",
                "authentication": "predefinedCredentialType", "nodeCredentialType": "anthropicApi",
                "sendHeaders": True, "headerParameters": {"parameters": [{"name": "anthropic-version", "value": "2023-06-01"}]},
                "sendBody": True, "specifyBody": "json",
                "jsonBody": '={{ {"model": "claude-sonnet-4-5-20250929", "max_tokens": 1024, "messages": [{"role": "user", "content": $json.prompt}]} }}',
                "options": {}
            },
            "id": "claude", "name": "Call Claude", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2,
            "position": [1120, 400],
            "credentials": {"anthropicApi": {"id": "REYgTvbzUh2zQgDS", "name": "x-api-key"}}
        },

        # Extract Analysis
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {"id": "analysis", "name": "analysis", "value": "={{ $json.content[0].text }}", "type": "string"},
                        {"id": "tokens", "name": "tokens", "value": "={{ $json.usage.input_tokens + $json.usage.output_tokens }}", "type": "number"},
                        {"id": "chat", "name": "chat_id", "value": "={{ $('Build Prompt').item.json.chat_id }}", "type": "string"},
                        {"id": "tg", "name": "send_telegram", "value": "={{ $('Build Prompt').item.json.send_telegram }}", "type": "boolean"},
                        {"id": "syms", "name": "symbols", "value": "={{ $('Build Prompt').item.json.symbols }}", "type": "string"}
                    ]
                }
            },
            "id": "extractAnalysis", "name": "Extract Analysis", "type": "n8n-nodes-base.set", "typeVersion": 3.3,
            "position": [1340, 400]
        },

        # If - Send Telegram?
        {
            "parameters": {"conditions": {"boolean": [{"value1": "={{ $json.send_telegram }}", "value2": True}]}},
            "id": "if", "name": "Send Telegram?", "type": "n8n-nodes-base.if", "typeVersion": 1,
            "position": [1560, 400]
        },

        # Send to Telegram
        {
            "parameters": {
                "chatId": "={{ $json.chat_id }}", "text": "={{ $json.analysis }}",
                "additionalFields": {"disable_web_page_preview": True, "parse_mode": "Markdown"}
            },
            "id": "telegram", "name": "Send to Telegram", "type": "n8n-nodes-base.telegram", "typeVersion": 1.1,
            "position": [1780, 300],
            "credentials": {"telegramApi": {"id": "RU8X7kcB4vm0KAFx", "name": "Telegram API"}}
        },

        # Telegram Response
        {
            "parameters": {
                "assignments": {
                    "assignments": [
                        {"id": "tg_sent", "name": "telegram_sent", "value": True, "type": "boolean"},
                        {"id": "tg_id", "name": "telegram_message_id", "value": "={{ $json.result.message_id }}", "type": "number"}
                    ]
                }
            },
            "id": "tgResponse", "name": "Telegram Response", "type": "n8n-nodes-base.set", "typeVersion": 3.3,
            "position": [2000, 300]
        },

        # No Telegram
        {
            "parameters": {
                "assignments": {
                    "assignments": [{"id": "no_tg", "name": "telegram_sent", "value": False, "type": "boolean"}]
                }
            },
            "id": "noTg", "name": "No Telegram", "type": "n8n-nodes-base.set", "typeVersion": 3.3,
            "position": [1780, 500]
        },

        # Merge
        {"parameters": {}, "id": "merge", "name": "Merge", "type": "n8n-nodes-base.merge", "typeVersion": 3, "position": [2220, 400]},

        # Respond
        {
            "parameters": {
                "respondWith": "json",
                "responseBody": '={{ {"success": true, "symbols": $("Extract Analysis").item.json.symbols, "analysis": $("Extract Analysis").item.json.analysis, "tokens_used": $("Extract Analysis").item.json.tokens, "telegram_sent": $json.telegram_sent, "telegram_message_id": $json.telegram_message_id || null} }}',
                "options": {}
            },
            "id": "respond", "name": "Respond", "type": "n8n-nodes-base.respondToWebhook", "typeVersion": 1.1,
            "position": [2440, 400]
        }
    ],
    "connections": {
        "Webhook": {"main": [[{"node": "Extract Params", "type": "main", "index": 0}]]},
        "Extract Params": {"main": [[{"node": "Fetch Stock 1", "type": "main", "index": 0}, {"node": "Fetch Stock 2", "type": "main", "index": 0}, {"node": "Fetch Stock 3", "type": "main", "index": 0}]]},
        "Fetch Stock 1": {"main": [[{"node": "Build Prompt", "type": "main", "index": 0}]]},
        "Fetch Stock 2": {"main": [[{"node": "Build Prompt", "type": "main", "index": 0}]]},
        "Fetch Stock 3": {"main": [[{"node": "Build Prompt", "type": "main", "index": 0}]]},
        "Build Prompt": {"main": [[{"node": "Call Claude", "type": "main", "index": 0}]]},
        "Call Claude": {"main": [[{"node": "Extract Analysis", "type": "main", "index": 0}]]},
        "Extract Analysis": {"main": [[{"node": "Send Telegram?", "type": "main", "index": 0}]]},
        "Send Telegram?": {"main": [[{"node": "Send to Telegram", "type": "main", "index": 0}], [{"node": "No Telegram", "type": "main", "index": 0}]]},
        "Send to Telegram": {"main": [[{"node": "Telegram Response", "type": "main", "index": 0}]]},
        "Telegram Response": {"main": [[{"node": "Merge", "type": "main", "index": 0}]]},
        "No Telegram": {"main": [[{"node": "Merge", "type": "main", "index": 1}]]},
        "Merge": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]}
    },
    "settings": {"executionOrder": "v1"}
}

print("📝 Creating workflow...")

create_response = requests.post(f"{N8N_URL}/api/v1/workflows", headers=headers, json=workflow)

if create_response.status_code in [200, 201]:
    created = create_response.json()
    workflow_id = created['id']

    print(f"✅ Created: {created['name']}")
    print(f"   ID: {workflow_id}")
    print(f"   Webhook: http://100.82.85.95:5678/webhook/stock-finnhub")

    # Save to .env
    with open('.env', 'a') as f:
        f.write(f"\nWORKFLOW_ID_FINNHUB_WORKING={workflow_id}\n")
        f.write(f"WEBHOOK_URL_FINNHUB_WORKING=http://100.82.85.95:5678/webhook/stock-finnhub\n")

    print(f"\n✅ Saved to .env")
    print(f"\n⚠️  Please activate it at: {N8N_URL}/workflows")
    print(f"\n" + "=" * 70)

else:
    print(f"❌ Failed: {create_response.status_code}")
    print(create_response.text)
