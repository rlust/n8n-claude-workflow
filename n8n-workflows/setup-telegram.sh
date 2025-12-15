#!/bin/bash

# Interactive Telegram setup and send script
# This helps you configure and send the testing summary to Telegram

set -e

echo "🤖 Telegram Summary Sender - Interactive Setup"
echo "=============================================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "📄 Found existing .env file. Loading..."
    source .env
    echo ""
fi

# Function to get Bot Token
get_bot_token() {
    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        echo "✅ Bot Token found in environment"
        echo "   Current token: ${TELEGRAM_BOT_TOKEN:0:20}..."
        read -p "   Use this token? (y/n): " use_existing
        if [ "$use_existing" = "y" ] || [ "$use_existing" = "Y" ]; then
            return
        fi
    fi

    echo ""
    echo "📋 How to get your Bot Token:"
    echo "   1. Open n8n at http://100.82.85.95:5678"
    echo "   2. Go to Settings → Credentials"
    echo "   3. Find 'Telegram API' credential"
    echo "   4. Copy the Access Token"
    echo ""
    read -p "Enter Bot Token: " TELEGRAM_BOT_TOKEN

    # Save to .env
    if grep -q "TELEGRAM_BOT_TOKEN" .env 2>/dev/null; then
        sed -i "s|TELEGRAM_BOT_TOKEN=.*|TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN|" .env
    else
        echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> .env
    fi
}

# Function to get Chat ID
get_chat_id() {
    if [ -n "$TELEGRAM_CHAT_ID" ]; then
        echo "✅ Chat ID found in environment"
        echo "   Current Chat ID: $TELEGRAM_CHAT_ID"
        read -p "   Use this Chat ID? (y/n): " use_existing
        if [ "$use_existing" = "y" ] || [ "$use_existing" = "Y" ]; then
            return
        fi
    fi

    echo ""
    echo "📋 How to get your Chat ID:"
    echo "   1. Send a message to your bot on Telegram"
    echo "   2. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
    echo "   3. Find the 'chat': {'id': XXXXXXX} in the response"
    echo ""
    read -p "Enter Chat ID: " TELEGRAM_CHAT_ID

    # Save to .env
    if grep -q "TELEGRAM_CHAT_ID" .env 2>/dev/null; then
        sed -i "s|TELEGRAM_CHAT_ID=.*|TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID|" .env
    else
        echo "TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID" >> .env
    fi
}

# Function to test credentials
test_credentials() {
    echo ""
    echo "🧪 Testing credentials..."

    response=$(curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\": \"${TELEGRAM_CHAT_ID}\", \"text\": \"✅ Test message from n8n testing summary bot\"}")

    if echo "$response" | grep -q '"ok":true'; then
        echo "✅ SUCCESS! Test message sent to Telegram"
        return 0
    else
        echo "❌ ERROR: Failed to send test message"
        echo "Response: $response"
        return 1
    fi
}

# Main flow
echo "Step 1: Configure Bot Token"
echo "----------------------------"
get_bot_token

echo ""
echo "Step 2: Configure Chat ID"
echo "-------------------------"
get_chat_id

echo ""
echo "Step 3: Test Connection"
echo "-----------------------"
if ! test_credentials; then
    echo ""
    echo "❌ Credentials test failed. Please check your token and chat ID."
    echo "   See get-telegram-credentials.md for help."
    exit 1
fi

echo ""
echo "Step 4: Send Summary"
echo "--------------------"
read -p "Send the full testing summary to Telegram? (y/n): " send_summary

if [ "$send_summary" = "y" ] || [ "$send_summary" = "Y" ]; then
    echo ""
    echo "📤 Sending summary..."
    ./send-to-telegram.sh "$TELEGRAM_BOT_TOKEN" "$TELEGRAM_CHAT_ID"
    echo ""
    echo "✅ Done! Check your Telegram for the summary."
else
    echo ""
    echo "⏭️  Skipped sending summary."
    echo "   You can send it later with:"
    echo "   ./send-to-telegram.sh"
fi

echo ""
echo "💾 Credentials saved to .env file"
echo "   Next time, just run: ./send-to-telegram.sh"
echo ""
