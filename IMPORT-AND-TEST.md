# Import and Test - Quick Guide

## Step 1: Import Workflow into n8n (Manual - 2 minutes)

Since I can't access the n8n web interface directly, you'll need to import it:

### Option A: Via n8n Web UI

1. **Open n8n:**
   ```
   http://100.82.85.95:5678
   ```

2. **Import workflow:**
   - Click "Add Workflow" (or the + button)
   - Click "Import from File"
   - Select: `n8n-workflows/examples/claude-stock-to-telegram.json`
   - Click "Import"

3. **Configure credentials:**
   - Click on "Call Claude API" node
   - Add/select your Anthropic API credentials
   - (Optional) Click on "Send to Telegram" node and add Telegram credentials

4. **Activate:**
   - Toggle "Active" switch to ON (top-right)
   - Note the webhook URL shown

### Option B: Via n8n CLI (if available)

```bash
# If you have n8n CLI access
n8n import:workflow --input=n8n-workflows/examples/claude-stock-to-telegram.json
```

## Step 2: Run Automated Tests

I created a comprehensive test script that will verify your workflow:

### Run All Tests

```bash
# Run full test suite
python3 test_stock_telegram.py --all
```

### Run Single Test

```bash
# Test specific stocks
python3 test_stock_telegram.py --symbols "AAPL,MSFT"

# Test with detailed analysis
python3 test_stock_telegram.py --symbols "TSLA,NVDA" --detailed

# Test market indices
python3 test_stock_telegram.py --symbols "^GSPC,^DJI"
```

### Test with Telegram (if configured)

```bash
python3 test_stock_telegram.py --symbols "AAPL,MSFT" --telegram --chat-id "YOUR_CHAT_ID"
```

### Different n8n URL

```bash
python3 test_stock_telegram.py --url "http://localhost:5678" --all
```

## Step 3: Manual curl Test (Alternative)

If the Python script doesn't work, test with curl:

```bash
# Basic test
curl -X POST http://100.82.85.95:5678/webhook/stock-to-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "AAPL,MSFT",
    "analysis_type": "overview",
    "send_to_telegram": false
  }'
```

## Expected Results

### Test Script Output

```
============================================================
🧪 Stock to Telegram Workflow Test Suite
============================================================

Testing workflow at: http://100.82.85.95:5678/webhook/stock-to-telegram
Timestamp: 2025-12-17T...

============================================================
Test 1: Check if workflow is active
============================================================

✓ Webhook endpoint is reachable

============================================================
Test: AAPL,MSFT (overview)
============================================================

ℹ Request payload:
{
  "symbols": "AAPL,MSFT",
  "analysis_type": "overview",
  "chat_id": "1955999067",
  "send_to_telegram": false
}

ℹ Sending request to webhook...

Response Status: 200
✓ Workflow executed successfully!
✓ Response indicates success
✓ Analysis text present
✓ Tokens used: 1234

============================================================
📊 Test Summary
============================================================

✓ Basic Test (AAPL,MSFT)
✓ Market Indices Test
✓ Detailed Analysis Test

Total: 3/3 tests passed

🎉 All tests passed!
```

## Troubleshooting

### "Cannot connect to n8n"
```bash
# Check if n8n is running
curl http://100.82.85.95:5678/healthz

# Check if you can access n8n UI
open http://100.82.85.95:5678
```

### "Webhook not found (404)"
- Make sure workflow is imported in n8n
- Make sure workflow is **Active** (toggle ON)
- Check webhook path is `/webhook/stock-to-telegram`

### "Internal server error (500)"
- Check n8n execution logs in the UI
- Verify Anthropic API credentials are configured
- Check n8n console for errors

### Python script issues
```bash
# Install requests if missing
pip3 install requests

# Run with Python 3
python3 test_stock_telegram.py --all
```

## What the Test Script Does

1. ✅ Checks if workflow webhook is accessible
2. 🧪 Tests basic stock analysis (AAPL, MSFT)
3. 📊 Tests market indices (S&P 500, Dow Jones)
4. 🔍 Tests detailed analysis mode
5. 📋 Provides detailed output and error messages
6. 📈 Shows test summary with pass/fail counts

## Next Steps After Testing

Once tests pass:

1. **Enable Telegram:**
   - Configure Telegram credentials in n8n
   - Test with `--telegram` flag

2. **Create scheduled runs:**
   - Add Cron node in n8n
   - Schedule daily market analysis

3. **Add more features:**
   - Price alerts
   - Portfolio tracking
   - News integration

---

**Need help?** Check the detailed guides:
- `STOCK-TO-TELEGRAM-QUICKSTART.md` - Setup and usage
- `STOCK-ANALYZER-TESTING.md` - Comprehensive testing guide
