# Claude Agent SDK Integration Guide for n8n

This guide shows you how to integrate the Claude Agent SDK into your n8n workflows for autonomous code execution and intelligent automation.

## What is Claude Agent SDK?

The Claude Agent SDK allows you to programmatically create Claude agents that can:
- **Read and write files** autonomously
- **Execute bash commands** to interact with systems
- **Search codebases** using Glob and Grep
- **Browse the web** for information
- **Maintain context** across multiple interactions
- **Return structured output** (JSON) for automation

Unlike simple Claude API calls, agents can perform multi-step tasks autonomously, making decisions and using tools to accomplish complex goals.

## Prerequisites

### 1. Environment Requirements

- n8n instance running (self-hosted or cloud)
- Python 3.8+ OR Node.js 16+ installed in n8n environment
- Anthropic API key

### 2. Install Claude Agent SDK

#### For Python-based n8n deployments:

```bash
# In your n8n container/environment
pip install claude-agent-sdk
```

#### For Node.js-based n8n deployments:

```bash
# In your n8n container/environment
npm install @anthropic-ai/claude-agent-sdk
```

### 3. Set Environment Variable

Add to your n8n environment:

```bash
export ANTHROPIC_API_KEY="sk-ant-api-your-key-here"
```

For Docker deployments, add to `docker-compose.yml`:

```yaml
environment:
  - ANTHROPIC_API_KEY=sk-ant-api-your-key-here
```

## Quick Start: Your First Agent Workflow

### Step 1: Import the Workflow

Import `examples/claude-agent-sdk-codebase-analyzer.json` into n8n:

1. Open n8n
2. Click **Workflows** → **Import from File**
3. Select the workflow file
4. Activate the workflow

### Step 2: Test the Agent

Send a POST request to trigger the agent:

```bash
curl -X POST http://localhost:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyze the Python files in this repository and list all functions",
    "repository_path": "/path/to/your/repo",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'
```

### Step 3: Review the Results

The agent will:
1. Explore the repository
2. Find Python files using Glob
3. Read and analyze them
4. Return a structured analysis

## Example Workflows

### Example 1: Automated Code Review

```json
{
  "task": "Review all JavaScript files for security issues, focusing on SQL injection and XSS vulnerabilities",
  "repository_path": "/app/src",
  "allowed_tools": ["Read", "Glob", "Grep"]
}
```

### Example 2: Documentation Generator

```json
{
  "task": "Generate a README.md file based on the code in this repository. Include setup instructions, usage examples, and API documentation",
  "repository_path": "/app",
  "allowed_tools": ["Read", "Write", "Glob", "Bash"]
}
```

### Example 3: Test Coverage Analysis

```json
{
  "task": "Analyze test coverage by comparing test files with source files. Identify which modules lack tests",
  "repository_path": "/app",
  "allowed_tools": ["Read", "Glob", "Grep", "Bash"]
}
```

### Example 4: Dependency Audit

```json
{
  "task": "Analyze package.json and requirements.txt files. List all dependencies and check for known security vulnerabilities",
  "repository_path": "/app",
  "allowed_tools": ["Read", "Bash", "WebSearch"]
}
```

## Advanced Usage

### Custom Python Agent in n8n

Create an **Execute Code** node with this Python code:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def run_custom_agent():
    task = $json.get('task')

    results = []
    async for message in query(
        prompt=task,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Bash", "Glob", "Grep"],
            permission_mode="acceptEdits",
            max_iterations=30,
            working_directory="/app",
            output_format="json"
        )
    ):
        # Capture messages
        if message.get("type") == "text":
            results.append(message.get("content"))

    return results

output = asyncio.run(run_custom_agent())
return [{"json": {"results": output}}]
```

### Custom TypeScript/JavaScript Agent in n8n

Create an **Execute Code** node with this JavaScript code:

```javascript
const { query } = require("@anthropic-ai/claude-agent-sdk");

async function runAgent() {
  const task = $json.task;
  const results = [];

  for await (const message of query({
    prompt: task,
    options: {
      allowedTools: ["Read", "Bash", "Glob"],
      permissionMode: "acceptEdits",
      maxIterations: 20,
      workingDirectory: "/app"
    }
  })) {
    if (message.type === "text") {
      results.push(message.content);
    }
  }

  return results;
}

const output = await runAgent();
return [{ json: { results: output } }];
```

## Available Tools

| Tool | Purpose | Use Case |
|------|---------|----------|
| **Read** | Read file contents | Analyzing code, config files |
| **Write** | Create/overwrite files | Generating docs, creating configs |
| **Edit** | Modify existing files | Refactoring, fixing bugs |
| **Bash** | Execute shell commands | Running tests, git operations |
| **Glob** | Find files by pattern | Locating specific file types |
| **Grep** | Search file contents | Finding code patterns, TODOs |
| **WebSearch** | Search the internet | Research, finding solutions |
| **WebFetch** | Fetch web pages | Reading documentation |

## Permission Modes

Control how the agent handles operations:

| Mode | Behavior | Use Case |
|------|----------|----------|
| `acceptEdits` | Auto-approve all operations | Trusted, automated workflows |
| `rejectEdits` | Deny all write operations | Read-only analysis |
| `confirmEdits` | Manual approval required | Interactive workflows |

## Real-World n8n Workflow Examples

### 1. GitHub PR Review Bot

```
GitHub Webhook (PR opened)
    ↓
Extract PR info
    ↓
Clone repository (Bash node)
    ↓
Run Claude Agent SDK (analyze changes)
    ↓
Post review comments (GitHub API)
```

### 2. Scheduled Documentation Update

```
Cron Trigger (weekly)
    ↓
Run Claude Agent SDK (generate docs)
    ↓
Git commit and push (Bash)
    ↓
Send summary email (Email node)
```

### 3. Code Quality Dashboard

```
HTTP Request (analyze endpoint)
    ↓
Run Claude Agent SDK (check quality)
    ↓
Store metrics (Database node)
    ↓
Update dashboard (API call)
```

### 4. Automated Refactoring Pipeline

```
Manual Trigger
    ↓
Run Claude Agent SDK (refactor code)
    ↓
Run tests (Bash)
    ↓
If tests pass → Create PR
    ↓
Notify team (Slack)
```

## Troubleshooting

### Issue: "claude-agent-sdk not installed"

**Solution:**
```bash
# Access your n8n container
docker exec -it n8n /bin/sh

# Install the SDK
pip install claude-agent-sdk
# OR
npm install @anthropic-ai/claude-agent-sdk

# Restart n8n
docker restart n8n
```

### Issue: "ANTHROPIC_API_KEY not found"

**Solution:**
Add to your environment:

```bash
# For Docker
docker run -e ANTHROPIC_API_KEY=your-key n8n

# For docker-compose.yml
environment:
  - ANTHROPIC_API_KEY=your-key
```

### Issue: Agent timeout or slow execution

**Solution:**
Adjust max_iterations and timeout:

```python
ClaudeAgentOptions(
    max_iterations=50,  # Increase for complex tasks
    timeout=300  # 5 minute timeout
)
```

### Issue: Permission denied errors

**Solution:**
Check file permissions and working directory:

```python
ClaudeAgentOptions(
    permission_mode="acceptEdits",
    working_directory="/app"  # Ensure n8n has access
)
```

## Best Practices

### 1. Clear Task Descriptions

✅ **Good:**
```
"Analyze all Python files in /app/src for security vulnerabilities. Focus on SQL injection, XSS, and hardcoded secrets. Return results as JSON with severity levels."
```

❌ **Bad:**
```
"Check the code"
```

### 2. Limit Tool Access

Only grant tools the agent needs:

```python
# For read-only analysis
allowed_tools=["Read", "Glob", "Grep"]

# For documentation generation
allowed_tools=["Read", "Write", "Glob"]

# For full automation
allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
```

### 3. Structure Output Requests

Ask for JSON output for easier parsing:

```
"Return your analysis as JSON with these keys:
- summary: overall assessment
- issues: array of problems found
- recommendations: suggested fixes"
```

### 4. Handle Errors Gracefully

```python
try:
    result = asyncio.run(run_agent())
    return [{"json": {"success": True, "result": result}}]
except Exception as e:
    return [{"json": {"success": False, "error": str(e)}}]
```

### 5. Monitor Token Usage

Agents can use significant tokens for complex tasks:

```python
# Add token tracking
async for message in query(prompt=task, options=options):
    if message.get("usage"):
        total_tokens = message["usage"].get("total_tokens")
        print(f"Tokens used: {total_tokens}")
```

## Cost Estimation

Using Claude Sonnet 4.5:

| Task Complexity | Iterations | Tokens | Cost (approx) |
|-----------------|-----------|--------|---------------|
| Simple file read | 1-3 | ~1,000 | $0.003 |
| Code analysis | 5-10 | ~5,000 | $0.015 |
| Refactoring | 10-20 | ~15,000 | $0.045 |
| Full codebase audit | 20-50 | ~50,000 | $0.150 |

## Performance Tips

### 1. Use Appropriate Models

```python
# For complex tasks
model="claude-opus-4-5-20251101"

# For balanced performance (default)
model="claude-sonnet-4-5-20250929"

# For simple, fast tasks
model="claude-haiku-3-5-20241022"
```

### 2. Cache Results

Store agent results in n8n variables or database to avoid re-running:

```javascript
// Check cache first
const cacheKey = `analysis_${repoHash}`;
const cached = $('GetFromCache').item.json.result;

if (cached) {
  return cached;
}

// Run agent only if not cached
const result = await runAgent();
```

### 3. Parallel Execution

For independent tasks, run multiple agents in parallel:

```
Split In Batches
    ↓
[Agent 1] [Agent 2] [Agent 3]
    ↓
Merge Results
```

## Security Considerations

### 1. Sandbox Agent Execution

```python
ClaudeAgentOptions(
    allowed_tools=["Read", "Glob"],  # No write/bash
    working_directory="/safe/path",   # Restricted directory
    permission_mode="rejectEdits"     # No modifications
)
```

### 2. Validate Input

```javascript
// In your n8n workflow
const task = $json.task;

// Sanitize and validate
if (!task || task.length > 1000) {
  throw new Error("Invalid task");
}
```

### 3. Rate Limiting

Use n8n's throttling or implement custom rate limits:

```javascript
// Check rate limit before running agent
const requestCount = $('CheckRateLimit').item.json.count;
if (requestCount > 10) {
  throw new Error("Rate limit exceeded");
}
```

## Next Steps

1. **Import the example workflow** and test it
2. **Customize the agent prompt** for your use case
3. **Integrate with your existing n8n workflows**
4. **Monitor performance and costs**
5. **Build production workflows** with error handling

## Resources

- **[Claude Agent SDK Docs](https://platform.claude.com/docs/en/agent-sdk/overview.md)** - Official documentation
- **[n8n Documentation](https://docs.n8n.io)** - n8n platform docs
- **[Anthropic API Docs](https://docs.anthropic.com)** - Claude API reference
- **[Example Workflows](./examples/)** - More workflow templates

## Support

For issues or questions:
- Check the [troubleshooting section](#troubleshooting)
- Review [n8n community forums](https://community.n8n.io)
- Consult [Anthropic documentation](https://docs.anthropic.com)

---

**Ready to automate with intelligent agents?** Import the example workflow and start building!
