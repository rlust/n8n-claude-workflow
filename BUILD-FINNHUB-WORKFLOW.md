# How to Build the Finnhub Stock Analysis Workflow in n8n

## 🎯 What We're Building

A workflow that:
- Accepts 3 stock symbols via webhook
- Fetches real-time data from Finnhub (in parallel)
- Analyzes with Claude
- Sends to Telegram
- Returns JSON response

---

## 📋 Step-by-Step Instructions

### Step 1: Create New Workflow

1. Go to: http://100.82.85.95:5678/workflows
2. Click **"Add workflow"** (top right)
3. Name it: **"Stock Analysis (Finnhub Manual)"**

---

### Step 2: Add Webhook Node

1. Click **"+" button** on canvas
2. Search for **"Webhook"**
3. Click to add it
4. Configure:
   - **HTTP Method:** POST
   - **Path:** `stock-finnhub-manual`
   - **Response Mode:** "Respond to Webhook"
5. Click **"Execute Node"** to register webhook

---

### Step 3: Add "Extract Parameters" Node

1. Click **"+"** after Webhook
2. Search for **"Edit Fields (Set)"**
3. Add these assignments:

| Field Name | Type | Value |
|------------|------|-------|
| `symbol1` | String | `={{ $json.body.symbols ? $json.body.symbols.split(',')[0]?.trim() : 'AAPL' }}` |
| `symbol2` | String | `={{ $json.body.symbols ? $json.body.symbols.split(',')[1]?.trim() : 'MSFT' }}` |
| `symbol3` | String | `={{ $json.body.symbols ? $json.body.symbols.split(',')[2]?.trim() : 'PRK' }}` |
| `chat_id` | String | `={{ $json.body.chat_id || '1955999067' }}` |
| `send_telegram` | Boolean | `={{ $json.body.send_to_telegram !== false }}` |

4. Name this node: **"Extract Params"**

---

### Step 4: Add HTTP Request for Stock 1

1. Click **"+"** after Extract Params
2. Search for **"HTTP Request"**
3. Configure:
   - **Method:** GET
   - **URL:** `https://finnhub.io/api/v1/quote?symbol={{ $json.symbol1 }}&token=cu6krs9r01qh2ki5u5tgcu6krs9r01qh2ki5u5u0`
4. Name it: **"Fetch Stock 1"**
5. Click **"Test step"** to verify it returns stock data

---

### Step 5: Add HTTP Requests for Stock 2 & 3

**For Stock 2:**
1. Go back to **"Extract Params"** node
2. Click **"+" button** (add another output)
3. Add another **HTTP Request** node
4. Configure:
   - **Method:** GET
   - **URL:** `https://finnhub.io/api/v1/quote?symbol={{ $json.symbol2 }}&token=cu6krs9r01qh2ki5u5tgcu6krs9r01qh2ki5u5u0`
5. Name it: **"Fetch Stock 2"**

**For Stock 3:**
1. Go back to **"Extract Params"** again
2. Add another **HTTP Request** node
3. Configure:
   - **Method:** GET
   - **URL:** `https://finnhub.io/api/v1/quote?symbol={{ $json.symbol3 }}&token=cu6krs9r01qh2ki5u5tgcu6krs9r01qh2ki5u5u0`
4. Name it: **"Fetch Stock 3"**

**Result:** You should have 3 HTTP nodes running in parallel from "Extract Params"

---

### Step 6: Add Merge Node

1. Click **"+"** anywhere on canvas
2. Search for **"Merge"**
3. Add it to canvas
4. **Connect all 3 stock fetch nodes to this Merge node:**
   - Click output dot of "Fetch Stock 1" → drag to Merge
   - Click output dot of "Fetch Stock 2" → drag to Merge
   - Click output dot of "Fetch Stock 3" → drag to Merge
5. Configure Merge node:
   - **Mode:** "Multiplex" (default is fine)
6. Name it: **"Merge Stocks"**

---

### Step 7: Add "Build Prompt" Code Node

1. Click **"+"** after Merge Stocks
2. Search for **"Code"**
3. Select **"Code" node**
4. Paste this JavaScript code:

```javascript
// Get all merged stock data
const items = $input.all();

// Get original parameters
const params = $('Extract Params').first().json;

// Process each stock
const stocks = items.map((item, index) => {
  const symbol = [params.symbol1, params.symbol2, params.symbol3][index];
  const data = item.json;

  if (data.c) {
    const price = data.c.toFixed(2);
    const change = (data.c - data.pc).toFixed(2);
    const changePct = (((data.c - data.pc) / data.pc) * 100).toFixed(2);
    return `${symbol}: $${price} (${change >= 0 ? '+' : ''}${changePct}%)`;
  }
  return `${symbol}: Data unavailable`;
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
```

5. Name it: **"Build Prompt"**

---

### Step 8: Add Claude API Call

1. Click **"+"** after Build Prompt
2. Search for **"HTTP Request"**
3. Configure:
   - **Method:** POST
   - **URL:** `https://api.anthropic.com/v1/messages`
   - **Authentication:** "Predefined Credential Type"
   - **Credential Type:** Select **"Anthropic API"** (your existing x-api-key)
   - **Send Headers:** ON
   - **Headers:**
     - Name: `anthropic-version`
     - Value: `2023-06-01`
   - **Send Body:** ON
   - **Body Content Type:** JSON
   - **JSON:**
```json
={{ {
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 1024,
  "messages": [{
    "role": "user",
    "content": $json.prompt
  }]
} }}
```

4. Name it: **"Call Claude"**

---

### Step 9: Extract Analysis

1. Click **"+"** after Call Claude
2. Add **"Edit Fields (Set)"** node
3. Add these fields:

| Field Name | Type | Value |
|------------|------|-------|
| `analysis` | String | `={{ $json.content[0].text }}` |
| `tokens` | Number | `={{ $json.usage.input_tokens + $json.usage.output_tokens }}` |
| `chat_id` | String | `={{ $('Build Prompt').item.json.chat_id }}` |
| `send_telegram` | Boolean | `={{ $('Build Prompt').item.json.send_telegram }}` |
| `symbols` | String | `={{ $('Build Prompt').item.json.symbols }}` |

4. Name it: **"Extract Analysis"**

---

### Step 10: Add Conditional (If) Node

1. Click **"+"** after Extract Analysis
2. Search for **"IF"**
3. Configure:
   - **Condition:** Boolean
   - **Value 1:** `={{ $json.send_telegram }}`
   - **Operation:** Equals
   - **Value 2:** `true`
4. Name it: **"Send Telegram?"**

---

### Step 11: Add Telegram Node (True Branch)

1. Click **"+"** on the **TRUE** output of If node
2. Search for **"Telegram"**
3. Configure:
   - **Credential:** Select your existing "Telegram API"
   - **Resource:** "Message"
   - **Operation:** "Send Message"
   - **Chat ID:** `={{ $json.chat_id }}`
   - **Text:** `={{ $json.analysis }}`
   - **Additional Fields:**
     - **Parse Mode:** Markdown
     - **Disable Web Page Preview:** Yes
4. Name it: **"Send to Telegram"**

---

### Step 12: Add Telegram Response Node

1. Click **"+"** after Send to Telegram
2. Add **"Edit Fields (Set)"** node
3. Add these fields:

| Field Name | Type | Value |
|------------|------|-------|
| `telegram_sent` | Boolean | `true` |
| `telegram_message_id` | Number | `={{ $json.result.message_id }}` |

4. Name it: **"Telegram Response"**

---

### Step 13: Add "No Telegram" Node (False Branch)

1. Click **"+"** on the **FALSE** output of If node
2. Add **"Edit Fields (Set)"** node
3. Add field:

| Field Name | Type | Value |
|------------|------|-------|
| `telegram_sent` | Boolean | `false` |

4. Name it: **"No Telegram"**

---

### Step 14: Add Final Merge

1. Add **"Merge"** node to canvas
2. Connect **"Telegram Response"** output → Merge
3. Connect **"No Telegram"** output → Merge
4. Name it: **"Merge Responses"**

---

### Step 15: Add Respond to Webhook Node

1. Click **"+"** after Merge Responses
2. Search for **"Respond to Webhook"**
3. Configure:
   - **Respond With:** JSON
   - **JSON:**
```json
={{ {
  "success": true,
  "symbols": $('Extract Analysis').item.json.symbols,
  "analysis": $('Extract Analysis').item.json.analysis,
  "tokens_used": $('Extract Analysis').item.json.tokens,
  "telegram_sent": $json.telegram_sent,
  "telegram_message_id": $json.telegram_message_id || null
} }}
```

4. Name it: **"Respond"**

---

## ✅ Final Steps

### Activate Workflow

1. Click **"Save"** (top right)
2. Toggle **"Active"** (top right)
3. You'll see: "Workflow activated"

---

## 🧪 Test Your Workflow

### Test 1: Without Telegram

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-finnhub-manual \
  -H 'Content-Type: application/json' \
  -d '{
    "symbols": "AAPL,MSFT,GOOGL",
    "send_to_telegram": false
  }'
```

**Expected:** JSON with real stock prices!

### Test 2: With Telegram

```bash
curl -X POST http://100.82.85.95:5678/webhook/stock-finnhub-manual \
  -H 'Content-Type: application/json' \
  -d '{
    "symbols": "AAPL,MSFT,PRK",
    "send_to_telegram": true
  }'
```

**Expected:** Analysis sent to Telegram + JSON response with message_id!

---

## 🎨 Visual Workflow Structure

```
Webhook
  ↓
Extract Params
  ├→ Fetch Stock 1 ──┐
  ├→ Fetch Stock 2 ──┼→ Merge Stocks
  └→ Fetch Stock 3 ──┘      ↓
                       Build Prompt
                            ↓
                       Call Claude
                            ↓
                      Extract Analysis
                            ↓
                      Send Telegram? (IF)
                       ↓           ↓
                  [TRUE]        [FALSE]
                      ↓              ↓
              Send to Telegram   No Telegram
                      ↓              ↓
            Telegram Response    (pass through)
                      ↓              ↓
                      └──→ Merge ←──┘
                            ↓
                         Respond
```

---

## 🔧 Troubleshooting

### Stock Data Not Showing?

1. Click **"Fetch Stock 1"** node
2. Click **"Test step"**
3. You should see: `{"c": 273.67, "h": 274.6, ...}`
4. If not, check:
   - URL has correct API key
   - Method is GET
   - Symbol expression is correct

### Claude Not Responding?

1. Check **"Call Claude"** node
2. Verify:
   - Credential is selected
   - Header `anthropic-version: 2023-06-01` is set
   - JSON body format is correct

### Telegram Not Sending?

1. Check **"Send Telegram?"** IF node
2. Click to see which branch executed
3. Verify Telegram credentials are set

---

## 📊 What You Get

✅ **Real-time stock data** from Finnhub (60 calls/min free)
✅ **AI analysis** from Claude
✅ **Telegram notifications**
✅ **JSON API** response
✅ **No more rate limiting** issues!

---

## 💡 Tips

- **Add more stocks:** Duplicate HTTP nodes and update Merge
- **Change symbols:** Pass different symbols in webhook body
- **Customize prompt:** Edit the Build Prompt code
- **Schedule it:** Add Cron trigger like your v3 workflow

---

**Your Finnhub API Key:** `cu6krs9r01qh2ki5u5tgcu6krs9r01qh2ki5u5u0`

**Webhook URL:** `http://100.82.85.95:5678/webhook/stock-finnhub-manual`

Good luck! 🚀
