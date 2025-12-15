# How to Get Telegram Bot Credentials from n8n

Since you mentioned there's already a working Telegram bot in n8n, here's how to get the credentials:

## Method 1: From n8n UI (Recommended)

1. **Access n8n:**
   ```
   http://100.82.85.95:5678
   ```

2. **Go to Credentials:**
   - Click on "Settings" (gear icon) in the left sidebar
   - Click on "Credentials"
   - Look for "Telegram API" credential

3. **View/Copy Credentials:**
   - Click on the Telegram credential
   - You'll see:
     - **Access Token** (Bot Token) - Looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
     - **Base URL** (optional) - Usually: `https://api.telegram.org`

4. **Get Chat ID:**
   - Send a message to your bot on Telegram
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Look for `"chat":{"id":XXXXXXX}` in the response
   - That number is your Chat ID

## Method 2: From n8n Workflow

If you have a workflow that uses Telegram:

1. Open any workflow that uses Telegram
2. Click on the Telegram node
3. View the credential reference
4. Go to Settings → Credentials to see the actual values

## Method 3: From Bot Configuration

If you created the bot yourself:

1. **Bot Token:**
   - Open Telegram
   - Search for @BotFather
   - Send `/mybots`
   - Select your bot
   - Click "API Token" to see it

2. **Chat ID:**
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Find the chat ID in the JSON response

## Once You Have the Credentials

Run the send script:

```bash
cd /root/claude/n8n-workflows

# Method 1: Pass as arguments
./send-to-telegram.sh <BOT_TOKEN> <CHAT_ID>

# Method 2: Set environment variables
export TELEGRAM_BOT_TOKEN="your-bot-token-here"
export TELEGRAM_CHAT_ID="your-chat-id-here"
./send-to-telegram.sh

# Method 3: Save to .env file
echo "TELEGRAM_BOT_TOKEN=your-token" > .env
echo "TELEGRAM_CHAT_ID=your-chat-id" >> .env
source .env
./send-to-telegram.sh
```

## Test the Bot First

Quick test to verify credentials work:

```bash
BOT_TOKEN="your-token-here"
CHAT_ID="your-chat-id-here"

curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"Test message\"}"
```

If you see `"ok":true` in the response, your credentials are working!
