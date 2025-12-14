# Quick Test Guide - Claude Agent SDK in n8n

## ⚡ Quick Start

### Option 1: Test via n8n UI (Simple Task Runner)

1. Go to http://100.82.85.95:5678
2. Open workflow: **"Claude Agent SDK - Simple Task Runner"**
3. Click **"Test workflow"** button
4. Watch the agent work autonomously!

**Default task**: Finds TODO comments in Python files

**Try modifying the task to**:
- "Count all JavaScript files in /tmp"
- "Find all functions in Python files"
- "List all markdown files and their sizes"

### Option 2: Test via API (Codebase Analyzer)

```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "YOUR TASK HERE",
    "repository_path": "/tmp",
    "allowed_tools": ["Read", "Bash", "Glob", "Grep"]
  }'
```

## 🎯 5-Minute Test Scenarios

### 1. Find TODO Comments
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find all TODO comments and list them",
    "repository_path": "/tmp",
    "allowed_tools": ["Grep", "Glob"]
  }'
```

### 2. Count Files by Type
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Count how many files of each type exist",
    "repository_path": "/tmp",
    "allowed_tools": ["Bash", "Glob"]
  }'
```

### 3. Security Scan
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find hardcoded API keys or passwords",
    "repository_path": "/tmp",
    "allowed_tools": ["Grep", "Read"]
  }'
```

### 4. List Directory Contents
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "List and describe what files are in /tmp",
    "repository_path": "/tmp",
    "allowed_tools": ["Bash"]
  }'
```

### 5. Analyze Dependencies
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Read package.json and list all dependencies",
    "repository_path": "/app",
    "allowed_tools": ["Read", "Bash"]
  }'
```

## 🔧 Available Tools

| Tool | What It Does | When to Use |
|------|-------------|-------------|
| **Read** | Read file contents | Viewing code, configs |
| **Bash** | Run shell commands | File operations, system info |
| **Glob** | Find files by pattern | Locating specific files |
| **Grep** | Search in files | Finding text patterns |
| **Write** | Create files | Generating reports |
| **Edit** | Modify files | Code fixes |

## 📊 What You'll See

**Agent working autonomously:**
```json
{
  "success": true,
  "analysis": "I found 23 TODO comments across 12 files:

**High Priority:**
- src/auth.js:45 - TODO: Add rate limiting
- src/api.js:128 - TODO: Implement error handling

**Medium Priority:**
- src/utils.js:67 - TODO: Add input validation
...",
  "metadata": {
    "messages_count": 15,
    "task": "Find all TODO comments",
    "timestamp": "2025-12-14T..."
  }
}
```

## 🎬 What Happens Behind the Scenes

**Your request**: "Find TODO comments in Python files"

**Agent's autonomous steps**:
1. 🔍 Uses **Glob** to find `*.py` files
2. 🔎 Uses **Grep** to search for "TODO"
3. 📖 Uses **Read** to get context
4. 🧠 Organizes and analyzes findings
5. 📝 Returns structured report

**You just see the final result!**

## 🚀 Run All Tests

We've created a test script for you:

```bash
cd /root/claude/n8n-workflows
./test-agent-workflows.sh
```

This runs 5 different test scenarios automatically!

## ⚙️ Prerequisites Checklist

Before testing, ensure:

- [ ] Workflows are **active** in n8n
- [ ] **ANTHROPIC_API_KEY** environment variable is set
- [ ] Agent SDK is installed:
  - `npm install @anthropic-ai/claude-agent-sdk` (for JS workflow)
  - `pip install claude-agent-sdk` (for Python workflow)

## 🔗 Full Documentation

- **[TESTING-AGENT-SDK.md](./TESTING-AGENT-SDK.md)** - Complete test guide with 20+ examples
- **[AGENT-SDK-GUIDE.md](./AGENT-SDK-GUIDE.md)** - Full setup and configuration guide
- **[README.md](./README.md)** - All workflows documentation

## 💡 Pro Tips

1. **Start simple**: Test with basic directory listings first
2. **Be specific**: "Find TODO comments in /src/components" > "Check code"
3. **Limit tools**: Only give tools the agent needs
4. **Check logs**: View execution details in n8n UI
5. **Iterate**: Refine your task descriptions based on results

## 🆘 Quick Troubleshooting

**"SDK not installed"** → Install: `npm install @anthropic-ai/claude-agent-sdk`

**"API key not found"** → Set: `export ANTHROPIC_API_KEY=your-key`

**Agent times out** → Make task more specific or reduce scope

**Permission denied** → Check repository path is accessible

---

**Ready to test?** Pick a scenario above and try it now!
