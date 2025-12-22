# Complete Finnhub Setup - 3 Easy Steps

✅ **Your API key is VALID and ready to use!**

**API Key:** `cu6krs9r01qh2ki5u5tgcu6krs9r01qh2ki5u5u0`

---

## Step 1: Add Finnhub Credentials to n8n (2 minutes)

1. **Open:** http://100.82.85.95:5678/credentials

2. **Sign in** to n8n if prompted

3. **Click:** "Add Credential" button (top right)

4. **Search for:** "Finnhub API"

5. **Fill in:**
   - **Name:** `finnhubApi` (exactly this - case sensitive!)
   - **API Key:** `cu6krs9r01qh2ki5u5tgcu6krs9r01qh2ki5u5u0`

6. **Click:** "Save"

---

## Step 2: Activate the Workflow (30 seconds)

1. **Open:** http://100.82.85.95:5678/workflows

2. **Find:** "Stock to Telegram v4 (Finnhub)"

3. **Click:** The toggle switch to activate (should turn green)

---

## Step 3: Test It! (30 seconds)

Run this command in terminal:

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-telegram-v4-finnhub \
  -H 'Content-Type: application/json' \
  -d '{"symbols": "AAPL,MSFT", "send_to_telegram": false}'
```

**Expected result:**
```json
{
  "success": true,
  "symbols": "AAPL,MSFT",
  "analysis": "📊 *Stock Market Analysis*\n\nAPPL: $273.67 (+$1.48)...",
  "tokens_used": 450,
  "telegram_sent": false
}
```

---

## ✅ Done!

Your new Finnhub-powered workflow is ready! It's **much more reliable** than Yahoo Finance.

### Key Improvements:
- ✅ 60 API calls/minute (vs Yahoo's rate limiting)
- ✅ Real-time stock data
- ✅ No more "data unavailable" errors
- ✅ Official, stable API

---

## 🔗 Quick Links

- **n8n Credentials:** http://100.82.85.95:5678/credentials
- **n8n Workflows:** http://100.82.85.95:5678/workflows
- **Finnhub Dashboard:** https://finnhub.io/dashboard
- **Webhook URL:** http://100.82.85.95:5678/webhook/stock-telegram-v4-finnhub

---

## Need Help?

If you see errors:
1. Make sure credential name is exactly `finnhubApi`
2. Verify workflow is activated (green toggle)
3. Check execution logs at: http://100.82.85.95:5678/executions
