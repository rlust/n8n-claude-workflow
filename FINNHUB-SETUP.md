# Finnhub Stock Analysis Workflow Setup Guide

## 🎉 What's New?

I've created an **improved version** of your stock analysis workflow using **Finnhub API** instead of Yahoo Finance.

### Why Finnhub is Better:

| Feature | Yahoo Finance | Finnhub |
|---------|--------------|---------|
| **Rate Limiting** | Aggressive (causing failures) | 60 calls/minute (free) |
| **Reliability** | Unofficial API, breaks often | Official, stable API |
| **Data Quality** | Good when working | Real-time, accurate |
| **Authentication** | Complex workarounds | Simple API key |
| **Cost** | Free but unreliable | Free tier available |
| **Documentation** | None (unofficial) | [Comprehensive docs](https://finnhub.io/docs/api) |

## 📋 Workflow Details

- **Name:** Stock to Telegram v4 (Finnhub)
- **ID:** PE0Zu4YdMrsKaSh5
- **Webhook:** http://100.82.85.95:5678/webhook/stock-telegram-v4-finnhub
- **Status:** Created (needs Finnhub API key to activate)

## 🔧 Setup Instructions

### Step 1: Get Your Free Finnhub API Key

1. **Sign up for Finnhub (FREE):**
   - Visit: https://finnhub.io/register
   - Create account with email

2. **Get your API key:**
   - Go to: https://finnhub.io/dashboard
   - Copy your API key (looks like: `ctodfupr01qretc7a2dgctodfupr01qretc7a2e0`)

### Step 2: Add Finnhub Credentials to n8n

1. **Open n8n credentials page:**
   - Navigate to: http://100.82.85.95:5678/credentials

2. **Create new Finnhub credential:**
   - Click "Add Credential"
   - Search for "Finnhub API"
   - Name: `finnhubApi`
   - API Key: `<paste your key here>`
   - Click "Save"

### Step 3: Activate the Workflow

1. **Open the workflow:**
   - Go to: http://100.82.85.95:5678/workflows
   - Find: "Stock to Telegram v4 (Finnhub)"

2. **Activate it:**
   - Click the toggle switch to activate
   - Workflow should show as "Active"

## 🧪 Testing

### Test via Webhook (No Telegram)

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-telegram-v4-finnhub \
  -H 'Content-Type: application/json' \
  -d '{
    "symbols": "AAPL,MSFT",
    "send_to_telegram": false
  }'
```

### Test with Telegram

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-telegram-v4-finnhub \
  -H 'Content-Type: application/json' \
  -d '{
    "symbols": "AAPL,MSFT,PRK",
    "send_to_telegram": true
  }'
```

### Using Python

```python
import requests

webhook_url = "http://100.82.85.95:5678/webhook/stock-telegram-v4-finnhub"

response = requests.post(webhook_url, json={
    "symbols": "AAPL,MSFT,PRK,QQQ,F",
    "send_to_telegram": True
})

print(response.json())
```

## 📊 API Response Format

### Finnhub Response Structure:

```json
{
  "c": 182.52,      // Current price
  "h": 184.20,      // Today's high
  "l": 181.50,      // Today's low
  "o": 182.00,      // Opening price
  "pc": 181.80,     // Previous close
  "t": 1703097600   // Timestamp
}
```

### Workflow Extracts:

- **Symbol:** Passed through from request
- **Price:** `c` (current)
- **Previous Close:** `pc`
- **Change:** `c - pc`
- **Change %:** `((c - pc) / pc) * 100`

## 🔄 Scheduled Execution

The cron trigger runs at **9:30 AM Mon-Fri** automatically with default stocks:
- F (Ford)
- AAPL (Apple)
- PRK (Park National)
- QQQ (Nasdaq ETF)
- MSFT (Microsoft)

## 🆚 Comparison with v3

| Feature | v3 (Yahoo Finance) | v4 (Finnhub) |
|---------|-------------------|--------------|
| Data Source | Yahoo Finance | Finnhub |
| Rate Limit | ~5-10/min (breaks) | 60/min (stable) |
| Reliability | ⚠️ Medium | ✅ High |
| Setup | No credentials | API key required |
| Cost | Free | Free tier |
| Stock Data | When available | Real-time |

## 📁 Files

- **Workflow JSON:** `n8n-workflows/examples/claude-stock-to-telegram-v4-finnhub.json`
- **Change Log:** `finnhub_workflow_changes.txt`
- **Setup Guide:** This file

## 🔗 Resources

- [Finnhub API Documentation](https://finnhub.io/docs/api)
- [Stock Quote Endpoint](https://finnhub.io/docs/api/quote)
- [Finnhub Dashboard](https://finnhub.io/dashboard)
- [Free vs Paid Comparison](https://finnhub.io/pricing)

## 💡 Tips

1. **Free Tier Limits:**
   - 60 API calls/minute
   - Sufficient for personal use
   - Upgrade to paid for higher limits

2. **Best Practices:**
   - Cache results when possible
   - Don't poll too frequently
   - Monitor your API usage

3. **Troubleshooting:**
   - If stocks show "unavailable", check API key
   - Verify credential name is `finnhubApi`
   - Check workflow is activated
   - Review execution logs in n8n

## ✅ Next Steps

1. ✅ Sign up for Finnhub
2. ✅ Get API key
3. ✅ Add credentials to n8n
4. ✅ Activate workflow
5. ✅ Test with webhook
6. ✅ Enjoy reliable stock data!

---

**Created:** 2025-12-21
**Workflow ID:** PE0Zu4YdMrsKaSh5
**Status:** Ready for activation
