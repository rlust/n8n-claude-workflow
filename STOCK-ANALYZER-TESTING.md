# Testing Stock Market Analyzer with Telegram Notifications

This guide shows you how to test the stock analysis workflow and integrate it with Telegram notifications.

## Available Workflows

1. **claude-stock-market-analyzer.json** - Basic stock analyzer
2. **claude-stock-market-analyzer-v2.json** - Enhanced with data cleaning
3. **telegram-notification-webhook.json** - Telegram message sender

## Prerequisites

### 1. n8n Setup
- n8n running at `http://100.82.85.95:5678` (or your instance)
- Import the workflow JSON files into n8n

### 2. Anthropic API Credentials
```bash
# In n8n UI:
# Settings → Credentials → Add Credential → Anthropic API
# Name: x-api-key
# API Key: your-anthropic-api-key
```

### 3. Telegram Bot (for notifications)
Create a Telegram bot to receive notifications:

```bash
# 1. Message @BotFather on Telegram
/newbot

# 2. Follow prompts to create bot
# You'll receive: Bot Token (e.g., 123456:ABC-DEF1234ghIkl)

# 3. Get your Chat ID
# Start a chat with @userinfobot or:
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```

## Part 1: Test Stock Analyzer (Without Telegram)

### Setup in n8n

1. **Import the workflow:**
   - Open n8n UI
   - Click "Import from File"
   - Select `claude-stock-market-analyzer-v2.json`

2. **Activate the workflow:**
   - Click "Active" toggle in top-right
   - Note the webhook URL (e.g., `http://100.82.85.95:5678/webhook/stock-analysis`)

3. **Configure Anthropic credentials:**
   - Click on "Call Claude API" node
   - Select or add your Anthropic API credentials

### Test with curl

**Basic Test (Default Symbols):**
```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Analyze Specific Stocks:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "AAPL,MSFT",
    "analysis_type": "overview"
  }'
```

**Detailed Analysis:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "TSLA,NVDA",
    "analysis_type": "detailed"
  }'
```

**Market Indices:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "^GSPC,^DJI",
    "analysis_type": "overview"
  }'
```

### Expected Response

```json
{
  "success": true,
  "symbols": "AAPL,MSFT",
  "analysis": "# Stock Market Analysis\n\n## Apple Inc. (AAPL)\n...",
  "metadata": {
    "model": "claude-sonnet-4-5-20250929",
    "tokens_used": 1234,
    "analyzed_at": "2025-12-17T..."
  }
}
```

## Part 2: Test Telegram Notifications

### Setup in n8n

1. **Import Telegram workflow:**
   - Import `telegram-notification-webhook.json`

2. **Configure Telegram credentials:**
   - Settings → Credentials → Add Credential → Telegram API
   - Bot Token: Your bot token from @BotFather
   - Chat ID: Your personal chat ID (or leave default)

3. **Activate the workflow**

### Test Telegram Message

```bash
curl -X POST http://100.82.85.95:5678/webhook/send-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "message": "🤖 Test from n8n!",
    "chat_id": "YOUR_CHAT_ID",
    "parse_mode": "Markdown"
  }'
```

**With Markdown formatting:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/send-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "message": "📊 *Stock Analysis*\n\n✅ AAPL: $150.25 (+2.3%)\n✅ MSFT: $380.50 (+1.8%)",
    "parse_mode": "Markdown"
  }'
```

## Part 3: Combine Stock Analysis + Telegram

You have two options:

### Option A: Chain with curl (Quick Test)

```bash
#!/bin/bash
# 1. Get stock analysis
ANALYSIS=$(curl -s -X POST http://100.82.85.95:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{"symbols": "AAPL,MSFT", "analysis_type": "overview"}')

# 2. Extract the analysis text
MESSAGE=$(echo $ANALYSIS | jq -r '.analysis')

# 3. Send to Telegram
curl -X POST http://100.82.85.95:5678/webhook/send-telegram \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"$MESSAGE\", \"parse_mode\": \"Markdown\"}"
```

### Option B: Create Combined n8n Workflow (Recommended)

Create a new workflow in n8n:

```
Webhook → Extract Params → Fetch Yahoo Data → Call Claude → Send to Telegram → Respond
```

**Workflow structure:**
1. **Webhook** - Receive stock symbols request
2. **Fetch Stock Data** - Get data from Yahoo Finance
3. **Call Claude API** - Analyze the data
4. **Send to Telegram** - Send analysis to Telegram
5. **Respond** - Return success to webhook caller

I can create this combined workflow JSON if you'd like!

## Part 4: Python Test Script

Create a test script for easy testing:

```python
#!/usr/bin/env python3
import requests
import json

# Configuration
N8N_URL = "http://100.82.85.95:5678"
STOCK_WEBHOOK = f"{N8N_URL}/webhook/stock-analysis"
TELEGRAM_WEBHOOK = f"{N8N_URL}/webhook/send-telegram"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"  # Replace with your chat ID

def analyze_stocks(symbols, analysis_type="overview"):
    """Analyze stock symbols using n8n workflow"""
    payload = {
        "symbols": symbols,
        "analysis_type": analysis_type
    }

    response = requests.post(STOCK_WEBHOOK, json=payload)
    return response.json()

def send_to_telegram(message, chat_id=TELEGRAM_CHAT_ID):
    """Send message to Telegram"""
    payload = {
        "message": message,
        "chat_id": chat_id,
        "parse_mode": "Markdown"
    }

    response = requests.post(TELEGRAM_WEBHOOK, json=payload)
    return response.json()

def analyze_and_notify(symbols, analysis_type="overview"):
    """Analyze stocks and send results to Telegram"""
    print(f"📊 Analyzing {symbols}...")

    # Get analysis
    result = analyze_stocks(symbols, analysis_type)

    if result.get("success"):
        analysis = result["analysis"]
        print(f"✅ Analysis complete ({result['metadata']['tokens_used']} tokens)")

        # Send to Telegram
        print("📱 Sending to Telegram...")
        telegram_result = send_to_telegram(analysis)

        if telegram_result.get("success"):
            print(f"✅ Sent to Telegram (message ID: {telegram_result.get('telegram_message_id')})")
        else:
            print(f"❌ Telegram failed: {telegram_result}")
    else:
        print(f"❌ Analysis failed: {result}")

    return result

if __name__ == "__main__":
    # Test examples
    analyze_and_notify("AAPL,MSFT", "overview")
    # analyze_and_notify("TSLA,NVDA", "detailed")
    # analyze_and_notify("^GSPC,^DJI", "overview")  # Market indices
```

## Common Stock Symbols

**Tech Giants:**
- `AAPL` - Apple
- `MSFT` - Microsoft
- `GOOGL` - Google/Alphabet
- `AMZN` - Amazon
- `META` - Meta/Facebook
- `NVDA` - NVIDIA
- `TSLA` - Tesla

**Market Indices:**
- `^GSPC` - S&P 500
- `^DJI` - Dow Jones Industrial Average
- `^IXIC` - NASDAQ Composite
- `^RUT` - Russell 2000

**ETFs:**
- `SPY` - S&P 500 ETF
- `QQQ` - NASDAQ-100 ETF
- `DIA` - Dow Jones ETF
- `IWM` - Russell 2000 ETF

## Troubleshooting

### "Webhook not found" Error
```bash
# Check if workflow is active
# In n8n: Toggle "Active" switch to ON
```

### "Authentication failed" Error
```bash
# Check Anthropic API credentials in n8n
# Settings → Credentials → Anthropic API
```

### Telegram not receiving messages
```bash
# 1. Verify bot token
# 2. Verify chat ID
# 3. Make sure you've started a chat with the bot
# 4. Check n8n Telegram credentials
```

### Yahoo Finance data errors
```bash
# Use correct symbol format:
# - Stocks: AAPL, MSFT
# - Indices: ^GSPC, ^DJI (note the ^ prefix)
# - ETFs: SPY, QQQ
```

## Next Steps

1. **Schedule regular updates:**
   - Add a Cron node to trigger analysis daily
   - Send morning market summary to Telegram

2. **Add price alerts:**
   - Monitor specific stocks
   - Send alerts when price crosses thresholds

3. **Portfolio tracking:**
   - Track multiple portfolios
   - Send daily performance summaries

4. **Enhanced analysis:**
   - Add technical indicators
   - Include news sentiment
   - Compare historical performance

---

Need the combined workflow JSON? Let me know!
