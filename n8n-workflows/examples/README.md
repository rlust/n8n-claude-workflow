# n8n Workflow Examples

This directory contains ready-to-use n8n workflow files that you can import into your n8n instance.

---

## 📦 Available Workflows

### Claude API Workflows (Simple HTTP Calls)

#### 1. claude-text-processor.json
**Purpose:** Basic text processing using Claude API

**Features:**
- Manual trigger
- Simple text input
- Claude Sonnet 4.5 model
- Extracts response and token count

**Use Cases:**
- Text summarization
- Content generation
- Quick Q&A
- Language translation

---

#### 2. claude-code-analyzer.json
**Purpose:** Code analysis via webhook

**Features:**
- Webhook trigger at `/webhook/analyze-code`
- Accepts: code, language, analysis_type
- Returns structured analysis
- max_tokens: 4096

**Use Cases:**
- Code review automation
- Security vulnerability detection
- Performance optimization suggestions
- Best practices validation

**Example:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "function test() { var x = 1; }",
    "language": "javascript",
    "analysis_type": "review"
  }'
```

---

#### 3. claude-document-summarizer.json
**Purpose:** Document summarization with customization

**Features:**
- Webhook trigger at `/webhook/summarize-document`
- Input validation (min 100 chars)
- Customizable format (paragraph/bullets)
- Customizable length (short/medium/long)
- Compression ratio calculation

**Use Cases:**
- Document summarization
- Meeting notes condensing
- Article summaries
- Content curation

**Example:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/summarize-document \
  -H "Content-Type: application/json" \
  -d '{
    "document": "Long text here...",
    "format": "bullets",
    "length": "short"
  }'
```

---

### Claude Agent SDK Workflows (Autonomous Agents)

#### 4. claude-agent-sdk-simple.json
**Purpose:** Simple autonomous agent using JavaScript SDK

**Features:**
- Manual trigger
- JavaScript execution
- Uses `@anthropic-ai/claude-agent-sdk`
- Autonomous tool usage (Read, Glob, Grep)
- Streaming messages
- Max iterations: 20

**Use Cases:**
- Finding code patterns
- Analyzing test coverage
- Generating code summaries
- Exploring codebases

**Example Tasks:**
- "Find all TODO comments in Python files"
- "List all API endpoints"
- "Analyze project structure"

---

#### 5. claude-agent-sdk-codebase-analyzer.json
**Purpose:** Advanced codebase analysis using Python SDK

**Features:**
- Webhook trigger at `/webhook/agent-analyze-codebase`
- Python execution
- Uses `claude-agent-sdk` (Python)
- Customizable tool permissions
- Structured JSON output
- Error handling
- Max iterations: 20

**Use Cases:**
- Security audits
- Code quality analysis
- Documentation checks
- Dependency analysis
- Architecture review

**Example:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/agent-analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find all files with TODO comments",
    "repo_path": "/path/to/repository"
  }'
```

---

### Telegram Integration Workflow

#### 6. telegram-notification-webhook.json ⭐ NEW
**Purpose:** Send Telegram notifications via webhook

**Features:**
- Webhook trigger at `/webhook/send-telegram`
- Sends messages to Telegram
- Supports Markdown formatting
- Custom chat ID support
- Returns success response

**Use Cases:**
- Test result notifications
- Build status alerts
- System monitoring alerts
- General notifications

**Example:**
```bash
curl -X POST http://100.82.85.95:5678/webhook/send-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "message": "✅ Tests passed!",
    "parse_mode": "Markdown",
    "chat_id": "1955999067"
  }'
```

**Setup Guide:** See `N8N-TELEGRAM-SETUP.md`

---

## 🚀 Quick Import Guide

### Step 1: Access n8n
```
http://100.82.85.95:5678
```

### Step 2: Import Workflow
1. Click "+" or "Add workflow"
2. Click three dots (⋮) → "Import from File"
3. Select the JSON file you want
4. Click "Import"

### Step 3: Configure Credentials
1. Click on nodes that need credentials (red warning icon)
2. Select or create appropriate credentials:
   - **Claude API:** Anthropic API
   - **Telegram:** Telegram API

### Step 4: Activate
1. Toggle "Inactive" → "Active" at the top
2. Workflow is now running!

---

## 📋 Credential Requirements

### Anthropic API (Claude)
**Required for:** All Claude workflows

**Setup:**
1. Settings → Credentials → Add Credential
2. Select "Anthropic API"
3. Enter your API key
4. Save

### Telegram API
**Required for:** telegram-notification-webhook.json

**Setup:**
1. Settings → Credentials → Add Credential
2. Select "Telegram API"
3. Enter:
   - **Access Token:** Your bot token
   - **Base URL:** `https://api.telegram.org`
4. Save

**Current Bot:**
- Username: @stockdata_from_n8n_bot
- Token: `8565077852:AAEvd5wvEnL3oJ1PgT981rnnrfO1NChyGy0`
- Chat ID: `1955999067`

---

## 🧪 Testing the Workflows

### Test Scripts Available

Located in `/root/claude/n8n-workflows/`:

**For Simple Workflows:**
```bash
./test-webhook.sh
```

**For Agent Workflows:**
```bash
./test-agent-workflows.sh
```

**For Telegram:**
```bash
./send-via-n8n.sh
```

---

## 📊 Workflow Comparison

| Workflow | Type | Trigger | Complexity | Use Case |
|----------|------|---------|------------|----------|
| text-processor | API | Manual | ⭐ Simple | Quick text tasks |
| code-analyzer | API | Webhook | ⭐⭐ Medium | Code review |
| document-summarizer | API | Webhook | ⭐⭐ Medium | Doc summaries |
| agent-sdk-simple | Agent | Manual | ⭐⭐⭐ Advanced | Autonomous tasks |
| agent-codebase-analyzer | Agent | Webhook | ⭐⭐⭐⭐ Expert | Complex analysis |
| telegram-notification | Integration | Webhook | ⭐ Simple | Notifications |

---

## 🔧 Customization Tips

### Modify Prompts
Edit the "Set" nodes to change system prompts and instructions.

### Adjust Token Limits
Change `max_tokens` in HTTP Request nodes:
- Simple tasks: 1024
- Code analysis: 4096
- Complex analysis: 8192

### Add Error Handling
Add "On Error" connections to handle failures gracefully.

### Chain Workflows
Use HTTP Request nodes to call other workflows via webhooks.

---

## 📚 Documentation

- **TESTING-AGENT-SDK.md** - Comprehensive testing guide
- **QUICK-TEST-GUIDE.md** - 5-minute quick start
- **N8N-TELEGRAM-SETUP.md** - Telegram setup guide
- **../tests/README.md** - Automated testing docs

---

## 🆘 Troubleshooting

### Workflow not triggering?
- Check if workflow is **Active**
- Verify webhook URL is correct
- Check n8n logs in Executions tab

### API errors?
- Verify credentials are configured
- Check API key is valid
- Review rate limits

### Agent workflows timing out?
- Increase max_iterations
- Simplify the task
- Check repository path exists

---

## 🎯 Next Steps

1. **Import a workflow** - Start with text-processor
2. **Configure credentials** - Add your API keys
3. **Test it** - Use the test scripts
4. **Customize** - Modify for your needs
5. **Automate** - Set up automated testing

---

**Need help?** Check the main README or testing guides!

**Ready to automate?** Import a workflow and start testing! 🚀
