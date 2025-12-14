# Quick Start Guide

Get your n8n + Claude integration running in 5 minutes!

## Step 1: Get Your Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create Key**
5. Copy your API key (starts with `sk-ant-api...`)

## Step 2: Configure n8n Credentials

### Option A: Using HTTP Header Auth (Recommended)

1. Open n8n at http://100.82.85.95:5678
2. Click your profile icon → **Settings** → **Credentials**
3. Click **+ Add Credential**
4. Search for **"Header Auth"** or **"HTTP Header Auth"**
5. Fill in:
   - **Credential Name**: `Anthropic API`
   - **Name**: `x-api-key`
   - **Value**: Paste your API key
6. Click **Save**

### Option B: Using Generic Credential Type

If your n8n version doesn't have Header Auth:

1. Create a **Generic Credential Type**
2. Add a custom header:
   - Header: `x-api-key`
   - Value: Your API key

## Step 3: Import a Workflow

1. In n8n, go to **Workflows**
2. Click **Import from File**
3. Select `examples/claude-text-processor.json`
4. Click **Import**

## Step 4: Configure the Workflow

1. Open the imported workflow
2. Click on the **"Call Claude API"** node
3. In the **Authentication** dropdown:
   - Select **Predefined Credential Type**
   - Choose **Header Auth**
   - Select your **Anthropic API** credential
4. Save the workflow

## Step 5: Test It!

1. Click the **"Test workflow"** button in the top right
2. Watch it execute
3. Check the output in the **"Extract Response"** node
4. You should see Claude's response!

## Step 6: Try the Code Analyzer Webhook

1. Import `examples/claude-code-analyzer.json`
2. Configure credentials (same as above)
3. **Activate** the workflow (toggle in top right)
4. Click the **Webhook** node to see your webhook URL
5. Test it:

```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "function test() { var x = 1; }",
    "language": "javascript"
  }'
```

## What's Next?

- Modify the prompts in the workflows
- Create your own workflows
- Combine Claude with other n8n nodes (Slack, Gmail, databases, etc.)
- Check out the full README.md for more examples

## Troubleshooting

### "401 Unauthorized" Error
- Double-check your API key is correct
- Make sure the header name is exactly `x-api-key`
- Verify the credential is selected in the HTTP Request node

### "Workflow not found" or Webhook 404
- Make sure the workflow is **activated** (toggle switch)
- Check the webhook path matches your request
- Restart n8n if needed: `docker restart n8n-n8n-1`

### "Connection refused"
- Verify n8n is running: `docker ps | grep n8n`
- Start it if needed: `docker start n8n-n8n-1`
- Check port 5678 is accessible

## Quick Reference

### Claude Models
- **claude-sonnet-4-5-20250929** - Best balance (recommended)
- **claude-opus-4-5-20251101** - Most capable
- **claude-haiku-3-5-20241022** - Fastest & cheapest

### API Endpoint
```
POST https://api.anthropic.com/v1/messages
```

### Required Headers
```
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

### Minimal Request Body
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 1024,
  "messages": [
    {"role": "user", "content": "Hello, Claude!"}
  ]
}
```

## Need Help?

- Read the full [README.md](README.md)
- Check [Anthropic API Docs](https://docs.anthropic.com)
- Visit [n8n Community](https://community.n8n.io)
