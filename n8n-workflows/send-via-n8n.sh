#!/bin/bash

# Send summary to Telegram via n8n webhook
# This uses the n8n Telegram Notification Webhook workflow

set -e

echo "📤 Send Testing Summary via n8n Webhook"
echo "======================================="
echo ""

# Default n8n webhook URL
N8N_WEBHOOK_URL="${N8N_WEBHOOK_URL:-http://100.82.85.95:5678/webhook/send-telegram}"

# Load chat ID from .env if exists
if [ -f .env ]; then
    source .env
fi

CHAT_ID="${TELEGRAM_CHAT_ID:-1955999067}"

echo "Using n8n webhook: $N8N_WEBHOOK_URL"
echo "Sending to Chat ID: $CHAT_ID"
echo ""

# Create compact summary for Telegram
MESSAGE="🚀 *n8n Testing Suite - Implementation Complete*

✅ *Project:* n8n Claude Workflows Testing
📅 *Date:* $(date '+%Y-%m-%d')
🔗 *Repo:* github.com/rlust/n8n-claude-workflow

━━━━━━━━━━━━━━━━━━━━━
*📊 DELIVERABLES*

🧪 *Test Suite*
• 12+ automated tests with assertions
• 370+ lines of test code
• ResponseValidator helper class
• PerformanceTracker with SLA checks

🤖 *CI/CD Integration*
• GitHub Actions workflow
• Multi-version Python (3.9, 3.10, 3.11)
• Daily scheduled tests
• Coverage reporting

📚 *Documentation*
• tests/README.md (11KB)
• TESTING-QUICKSTART.md (3.5KB)
• Comprehensive guides

⚙️ *Infrastructure*
• Makefile with 8+ commands
• pytest.ini configuration
• .gitignore for Python

━━━━━━━━━━━━━━━━━━━━━
*🎯 KEY IMPROVEMENTS*

*Before:*
❌ Manual testing only
❌ No assertions
❌ No CI/CD

*After:*
✅ Automated validation
✅ Proper assertions
✅ GitHub Actions CI/CD
✅ 3,000+ lines added
✅ 22 files created

━━━━━━━━━━━━━━━━━━━━━
*🚀 QUICK START*

\`\`\`bash
make install
make test-fast
make test-coverage
\`\`\`

━━━━━━━━━━━━━━━━━━━━━
*⚠️ NEXT STEPS*

1️⃣ Activate n8n workflows
2️⃣ Configure Claude API key
3️⃣ Run: \`make test-fast\`

━━━━━━━━━━━━━━━━━━━━━

📋 *Full Summary:* IMPLEMENTATION-SUMMARY.md
📖 *Documentation:* tests/README.md

🤖 Generated with Claude Code"

echo "Sending to n8n..."
echo ""

# Send to n8n webhook
response=$(curl -s -X POST "$N8N_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "{
        \"message\": $(echo "$MESSAGE" | jq -Rs .),
        \"parse_mode\": \"Markdown\",
        \"chat_id\": \"$CHAT_ID\"
    }")

if [ $? -eq 0 ]; then
    # Check if response contains success
    if echo "$response" | grep -q '"success":true'; then
        echo "✅ Message sent successfully via n8n!"
        echo ""
        echo "Response:"
        echo "$response" | jq '.'
    else
        echo "⚠️  Request completed but check response:"
        echo "$response" | jq '.'
    fi
else
    echo "❌ Failed to send message"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check if n8n is running: curl http://100.82.85.95:5678"
    echo "2. Verify webhook URL: $N8N_WEBHOOK_URL"
    echo "3. Import telegram-notification-webhook.json into n8n"
    echo "4. Activate the workflow in n8n UI"
    echo "5. Set up Telegram API credentials in n8n"
    echo ""
    echo "Alternative: Use direct Telegram API with ./send-to-telegram.sh"
fi

echo ""
