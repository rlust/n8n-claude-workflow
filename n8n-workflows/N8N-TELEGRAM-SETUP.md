# 🔧 n8n Telegram Notification Workflow Setup Guide

This guide will help you set up the Telegram notification workflow in n8n.

---

## 📋 Prerequisites

Before you begin, you need:
- ✅ n8n running at http://100.82.85.95:5678
- ✅ Telegram bot token: `8565077852:AAEvd5wvEnL3oJ1PgT981rnnrfO1NChyGy0`
- ✅ Your chat ID: `1955999067`
- ✅ Workflow file: `examples/telegram-notification-webhook.json`

---

## 🚀 Setup Steps

### Step 1: Import the Workflow into n8n

1. **Open n8n**
   ```
   http://100.82.85.95:5678
   ```

2. **Create New Workflow**
   - Click the "+" button or "Add workflow" in the left sidebar

3. **Import from File**
   - Click the three dots menu (⋮) in the top right
   - Select "Import from File"
   - Choose `examples/telegram-notification-webhook.json`
   - Click "Import"

### Step 2: Set Up Telegram API Credentials

1. **Go to Credentials**
   - Click Settings (⚙️ gear icon) in left sidebar
   - Click "Credentials"
   - Click "Add Credential" button

2. **Create Telegram API Credential**
   - Search for "Telegram"
   - Select "Telegram API"
   - Enter details:
     - **Name:** `Telegram Bot (stockdata_from_n8n_bot)`
     - **Access Token:** `8565077852:AAEvd5wvEnL3oJ1PgT981rnnrfO1NChyGy0`
     - **Base URL:** `https://api.telegram.org` (default)
   - Click "Create"

3. **Link Credential to Workflow**
   - Go back to your imported workflow
   - Click on the "Send to Telegram" node
   - In the "Credential to connect with" dropdown
   - Select the credential you just created
   - Click "Save" or the checkmark

### Step 3: Activate the Workflow

1. **In the Workflow Editor**
   - Find the toggle switch at the top that says "Inactive"
   - Click it to turn it to "Active"
   - The workflow is now listening for webhook requests!

2. **Get the Webhook URL**
   - Click on the "Webhook Trigger" node
   - You'll see the webhook URL (should be similar to):
     ```
     http://100.82.85.95:5678/webhook/send-telegram
     ```
   - Copy this URL for later use

### Step 4: Test the Workflow

**Option A: Test in n8n UI**
1. Click on the "Webhook Trigger" node
2. Click "Listen for test event"
3. Use the shell script to send a test:
   ```bash
   cd /root/claude/n8n-workflows
   ./send-via-n8n.sh
   ```
4. Check n8n UI - you should see the execution
5. Check Telegram - you should receive the message!

**Option B: Use curl directly**
```bash
curl -X POST http://100.82.85.95:5678/webhook/send-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Test from n8n webhook!",
    "parse_mode": "Markdown",
    "chat_id": "1955999067"
  }'
```

---

## 🎯 How to Use

### Method 1: Using the Shell Script

```bash
cd /root/claude/n8n-workflows

# Send via n8n webhook
./send-via-n8n.sh

# Or with custom webhook URL
N8N_WEBHOOK_URL="http://100.82.85.95:5678/webhook/send-telegram" ./send-via-n8n.sh
```

### Method 2: Direct API Call

```bash
curl -X POST http://100.82.85.95:5678/webhook/send-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Your message here",
    "parse_mode": "Markdown",
    "chat_id": "1955999067"
  }'
```

### Method 3: From Other n8n Workflows

Add an HTTP Request node to any workflow:
- **Method:** POST
- **URL:** `http://100.82.85.95:5678/webhook/send-telegram`
- **Body (JSON):**
  ```json
  {
    "message": "{{ $json.yourMessage }}",
    "parse_mode": "Markdown",
    "chat_id": "1955999067"
  }
  ```

---

## 📊 Workflow Details

### What the Workflow Does

1. **Webhook Trigger** - Listens for POST requests at `/webhook/send-telegram`
2. **Extract Parameters** - Extracts message, parse_mode, and chat_id
3. **Send to Telegram** - Sends the message using Telegram API
4. **Format Response** - Creates a success response
5. **Respond to Webhook** - Returns JSON response to caller

### Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| message | string | (required) | The message to send |
| parse_mode | string | "Markdown" | Formatting mode (Markdown, HTML, or none) |
| chat_id | string | "1955999067" | Telegram chat ID to send to |

### Response Format

**Success:**
```json
{
  "success": true,
  "message": "Message sent successfully to Telegram",
  "telegram_message_id": 123,
  "chat_id": "1955999067",
  "timestamp": "2025-12-15T16:00:00.000Z"
}
```

**Error:**
If the Telegram API fails, n8n will return an error response.

---

## 🔍 Troubleshooting

### Issue 1: "Workflow is not active"
**Solution:**
- Open the workflow in n8n
- Click the "Inactive" toggle to make it "Active"

### Issue 2: "Credential not found"
**Solution:**
1. Go to Settings → Credentials
2. Create a new Telegram API credential
3. Go back to workflow
4. Click "Send to Telegram" node
5. Select your credential

### Issue 3: "Webhook not found (404)"
**Solution:**
- Verify the workflow is active
- Check the webhook URL matches: `/webhook/send-telegram`
- The workflow must be saved and active

### Issue 4: "Unauthorized (401)"
**Solution:**
- Check your bot token is correct
- Verify it matches: `8565077852:AAEvd5wvEnL3oJ1PgT981rnnrfO1NChyGy0`
- Test the token: `curl https://api.telegram.org/bot<TOKEN>/getMe`

### Issue 5: "Chat not found"
**Solution:**
- Make sure you've sent at least one message to the bot first
- Verify your chat ID is correct: `1955999067`

---

## 🎓 Advanced Usage

### Custom Message Templates

Create different message types by modifying the request:

**Simple Alert:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/send-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "message": "🚨 Alert: Test failed!",
    "chat_id": "1955999067"
  }'
```

**Formatted Report:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/send-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "message": "*Build Status*\n\n✅ Tests: Passed\n⏱ Duration: 2m 30s",
    "parse_mode": "Markdown",
    "chat_id": "1955999067"
  }'
```

### Multiple Recipients

To send to multiple chat IDs, call the webhook multiple times or modify the workflow to accept an array of chat IDs.

### Schedule Notifications

Create a Cron node in n8n:
1. Add a Cron node
2. Set schedule (e.g., daily at 9 AM)
3. Connect to an HTTP Request node
4. Point it to your webhook
5. Send daily reports automatically!

---

## 📚 Related Files

- **telegram-notification-webhook.json** - The workflow file
- **send-via-n8n.sh** - Shell script to use the webhook
- **send-to-telegram.sh** - Direct Telegram API script (alternative)
- **setup-telegram.sh** - Interactive setup for direct API
- **TELEGRAM-GUIDE.md** - Complete Telegram integration guide

---

## 🔄 Comparison: n8n vs Direct API

### Use n8n Webhook When:
- ✅ You want centralized notification management
- ✅ You need to track/log all notifications in n8n
- ✅ You want to add custom logic (filtering, transformations)
- ✅ You want to integrate with other n8n workflows
- ✅ You need rate limiting or queuing

### Use Direct API When:
- ✅ You want simple, fast notifications
- ✅ You're running from scripts/cron
- ✅ You don't need n8n features
- ✅ You want minimal dependencies

**Both methods work great - choose based on your needs!**

---

## ✅ Verification Checklist

After setup, verify:

- [ ] n8n is running and accessible
- [ ] Workflow imported successfully
- [ ] Telegram API credential created
- [ ] Credential linked to "Send to Telegram" node
- [ ] Workflow is **Active** (not Inactive)
- [ ] Webhook URL is correct
- [ ] Test message sent successfully
- [ ] Message received in Telegram
- [ ] Shell script works: `./send-via-n8n.sh`

---

## 🆘 Need Help?

**Check n8n execution log:**
1. Go to "Executions" tab in n8n
2. Find your workflow execution
3. Click to see details
4. Check for errors

**Test bot token:**
```bash
curl https://api.telegram.org/bot8565077852:AAEvd5wvEnL3oJ1PgT981rnnrfO1NChyGy0/getMe
```

**Check if workflow is active:**
```bash
curl http://100.82.85.95:5678/webhook/send-telegram
# Should return: "This webhook is not registered for GET requests"
# If 404, workflow is not active
```

---

**Setup complete?** Run `./send-via-n8n.sh` to test! 🚀
