# Quick Finnhub Setup (5 Minutes)

## Step 1: Get API Key (2 min)

1. **Go to:** https://finnhub.io/register
   - Enter email & password
   - Click "Sign Up"

2. **Go to:** https://finnhub.io/dashboard
   - Copy your API key (it's displayed prominently)
   - It looks like: `ctodfupr01qretc7a2dgctodfupr01qretc7a2e0`

## Step 2: Add to n8n (2 min)

1. **Go to:** http://100.82.85.95:5678/credentials

2. **Click:** "Add Credential" (top right)

3. **Search for:** "Finnhub API"

4. **Fill in:**
   - Name: `finnhubApi`
   - API Key: `<paste your key here>`

5. **Click:** "Save"

## Step 3: Activate Workflow (1 min)

1. **Go to:** http://100.82.85.95:5678/workflows

2. **Find:** "Stock to Telegram v4 (Finnhub)"

3. **Click:** The toggle switch to activate (should turn green)

## Step 4: Test It!

Run this in terminal:
```bash
python3 test_finnhub_workflow.py
```

Or test with curl:
```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-telegram-v4-finnhub \
  -H 'Content-Type: application/json' \
  -d '{"symbols": "AAPL,MSFT", "send_to_telegram": false}'
```

✅ **Done!** You should see real stock data now instead of "unavailable"!

## Troubleshooting

**If you see "unavailable" or errors:**
1. Check API key is correct at https://finnhub.io/dashboard
2. Verify credential name is exactly `finnhubApi` (case-sensitive)
3. Make sure workflow is activated (green toggle)
4. Check n8n execution logs at http://100.82.85.95:5678/executions
