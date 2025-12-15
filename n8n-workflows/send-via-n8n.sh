#!/bin/bash

# Send summary to Telegram via n8n webhook
# This uses your existing n8n Telegram integration

set -e

echo "📤 Send Testing Summary via n8n Webhook"
echo "======================================="
echo ""

# Default n8n webhook URL (update this if different)
N8N_WEBHOOK_URL="${N8N_WEBHOOK_URL:-http://100.82.85.95:5678/webhook/send-telegram}"

# Read the summary
SUMMARY=$(cat IMPLEMENTATION-SUMMARY.md)

echo "Using n8n webhook: $N8N_WEBHOOK_URL"
echo ""

# Create compact summary for Telegram
MESSAGE="🚀 *n8n Testing Suite - Complete*

📊 *Deliverables:*
✅ 12+ automated tests with pytest
✅ GitHub Actions CI/CD workflow
✅ ResponseValidator & PerformanceTracker
✅ 30KB+ comprehensive documentation
✅ Makefile with 8+ commands

📈 *Stats:*
• Files: 17 created (3,000+ lines)
• Tests: 12+ with assertions
• Docs: tests/README.md (11KB)
• Commit: dcfcd82

⚙️ *Next Steps:*
1. Activate n8n workflows
2. Configure Claude API key
3. Run: \`make test-fast\`

📋 Full details in repo:
github.com/rlust/n8n-claude-workflow

🤖 Generated with Claude Code"

echo "Sending to n8n..."
echo ""

# Send to n8n webhook
response=$(curl -s -X POST "$N8N_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "{
        \"message\": $(echo "$MESSAGE" | jq -Rs .),
        \"parse_mode\": \"Markdown\"
    }")

if [ $? -eq 0 ]; then
    echo "✅ Message sent to n8n webhook"
    echo ""
    echo "Response: $response"
else
    echo "❌ Failed to send message"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check if n8n is running: curl http://100.82.85.95:5678"
    echo "2. Verify webhook URL: $N8N_WEBHOOK_URL"
    echo "3. Check if webhook is active in n8n UI"
    echo ""
    echo "Alternative: Use direct Telegram API with ./setup-telegram.sh"
fi

echo ""
