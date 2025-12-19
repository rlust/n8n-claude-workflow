# Stock Analysis to Telegram - Quick Start Guide

## What This Workflow Does

📊 **Fetches** stock data from Yahoo Finance
🤖 **Analyzes** with Claude AI
📱 **Sends** results to Telegram (optional)
✅ **Returns** webhook response with analysis

## Setup (5 minutes)

### 1. Import into n8n

```bash
# In n8n UI:
# 1. Click "Add Workflow" → "Import from File"
# 2. Select: n8n-workflows/examples/claude-stock-to-telegram.json
# 3. Click "Import"
```

### 2. Configure Credentials

**Anthropic API:**
- Go to: Settings → Credentials → Add Credential
- Type: Anthropic API
- Name: `x-api-key`
- API Key: Your Anthropic API key from console.anthropic.com

**Telegram Bot (Optional):**
- Go to: Settings → Credentials → Add Credential
- Type: Telegram API
- Name: `Telegram API`
- Bot Token: Get from @BotFather on Telegram
- Chat ID: Your Telegram chat ID

### 3. Activate Workflow

- Toggle "Active" switch to ON
- Note your webhook URL: `http://YOUR_N8N_URL:5678/webhook/stock-to-telegram`

## Usage Examples

### Basic Test (With Telegram)

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-to-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "AAPL,MSFT",
    "analysis_type": "overview",
    "chat_id": "YOUR_CHAT_ID"
  }'
```

### Detailed Analysis

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-to-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "TSLA,NVDA",
    "analysis_type": "detailed",
    "chat_id": "YOUR_CHAT_ID"
  }'
```

### Without Telegram (API only)

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-to-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "^GSPC,^DJI",
    "analysis_type": "overview",
    "send_to_telegram": false
  }'
```

### Market Indices

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-to-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "^GSPC,^DJI",
    "chat_id": "YOUR_CHAT_ID"
  }'
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `symbols` | No | `AAPL,MSFT` | Comma-separated stock symbols |
| `analysis_type` | No | `overview` | `overview` or `detailed` |
| `chat_id` | No | `1955999067` | Your Telegram chat ID |
| `send_to_telegram` | No | `true` | Whether to send to Telegram |

## Expected Response

**With Telegram:**
```json
{
  "success": true,
  "message": "Stock analysis sent to Telegram successfully",
  "telegram_message_id": 12345,
  "analysis": "📊 *Stock Market Analysis*...",
  "symbols": "AAPL,MSFT",
  "tokens_used": 1234
}
```

**Without Telegram:**
```json
{
  "success": true,
  "message": "Stock analysis completed (Telegram disabled)",
  "analysis": "📊 *Stock Market Analysis*...",
  "symbols": "AAPL,MSFT",
  "tokens_used": 1234,
  "telegram_sent": false
}
```

## Telegram Message Format

The analysis will appear in Telegram formatted like:

```
📊 *Stock Market Analysis*

🍎 *Apple Inc. (AAPL)*
Current: $150.25 (+2.3%)
Trend: Bullish 📈

🪟 *Microsoft Corp. (MSFT)*
Current: $380.50 (+1.8%)
Trend: Stable 📊

💭 *Market Outlook*
Both stocks showing positive momentum...

📅 Analyzed: Dec 17, 2025
```

## Test Script (Python)

```python
#!/usr/bin/env python3
import requests

N8N_URL = "http://100.82.85.95:5678"
WEBHOOK = f"{N8N_URL}/webhook/stock-to-telegram"
CHAT_ID = "YOUR_CHAT_ID"  # Replace with your chat ID

def analyze_stocks(symbols, detailed=False, send_telegram=True):
    """Analyze stocks and optionally send to Telegram"""
    payload = {
        "symbols": symbols,
        "analysis_type": "detailed" if detailed else "overview",
        "chat_id": CHAT_ID,
        "send_to_telegram": send_telegram
    }

    response = requests.post(WEBHOOK, json=payload)
    result = response.json()

    if result.get("success"):
        print(f"✅ Analysis complete!")
        print(f"   Symbols: {result['symbols']}")
        print(f"   Tokens: {result['tokens_used']}")
        if result.get('telegram_message_id'):
            print(f"   Telegram: Sent (ID: {result['telegram_message_id']})")
        print(f"\n{result['analysis']}\n")
    else:
        print(f"❌ Failed: {result}")

    return result

# Test examples
if __name__ == "__main__":
    # Quick overview
    analyze_stocks("AAPL,MSFT")

    # Detailed analysis
    # analyze_stocks("TSLA,NVDA", detailed=True)

    # API only (no Telegram)
    # analyze_stocks("^GSPC,^DJI", send_telegram=False)
```

## Popular Stock Symbols

**Tech:**
- `AAPL` - Apple
- `MSFT` - Microsoft
- `GOOGL` - Google
- `AMZN` - Amazon
- `NVDA` - NVIDIA
- `TSLA` - Tesla
- `META` - Meta

**Market Indices:**
- `^GSPC` - S&P 500
- `^DJI` - Dow Jones
- `^IXIC` - NASDAQ

**ETFs:**
- `SPY` - S&P 500 ETF
- `QQQ` - NASDAQ-100
- `DIA` - Dow Jones ETF

## Troubleshooting

### "Webhook not found"
- Make sure workflow is **Active** (toggle ON)
- Check webhook URL matches your n8n instance

### "Authentication failed"
- Verify Anthropic API credentials in n8n
- Check API key is valid at console.anthropic.com

### Telegram not working
- Verify you've started a chat with your bot
- Check bot token and chat ID are correct
- Make sure `send_to_telegram: true` in request

### Yahoo Finance errors
- Use correct symbol format (AAPL, not Apple)
- For indices use `^` prefix (^GSPC, not GSPC)
- Check symbols exist on Yahoo Finance

## Next Steps

**Schedule Daily Updates:**
```
Add Cron node → Trigger at 9:30 AM → Run this workflow
```

**Add Price Alerts:**
```
Add condition node → Check if price > threshold → Send alert
```

**Multiple Portfolios:**
```
Create separate requests for different symbol groups
```

---

🎉 **Your workflow is ready!** Test it now with:

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-to-telegram \
  -H "Content-Type: application/json" \
  -d '{"symbols": "AAPL,MSFT", "chat_id": "YOUR_CHAT_ID"}'
```
