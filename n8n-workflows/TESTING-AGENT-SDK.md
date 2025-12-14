# Testing Claude Agent SDK Workflows in n8n

This guide shows you how to test the Claude Agent SDK workflows from your n8n instance.

## Prerequisites

Before testing, ensure you have:

1. **Anthropic API Key** set as environment variable:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-api-your-key-here"
   ```

2. **Agent SDK installed** (depending on which workflow you're testing):
   ```bash
   # For JavaScript workflows
   npm install @anthropic-ai/claude-agent-sdk

   # For Python workflows
   pip install claude-agent-sdk
   ```

3. **Workflows activated** in n8n (for webhook-based workflows)

## Test Scenarios

### 1. Simple Task Runner (Manual Trigger)

**Workflow**: Claude Agent SDK - Simple Task Runner

**How to test**:
1. Open the workflow in n8n at http://100.82.85.95:5678
2. Click on the **"Set Task"** node
3. Modify the task in the node settings
4. Click **"Test workflow"** button

**Example tasks to try**:

```javascript
// Task 1: Find TODO comments
"Find all TODO comments in JavaScript files in /tmp/test-repo and list them with file names and line numbers"

// Task 2: Count files by type
"Search the /app directory and count how many files of each type (.js, .py, .md) exist"

// Task 3: Check for security issues
"Search for hardcoded API keys or passwords in all files in /tmp/project. Look for patterns like 'api_key=', 'password=', or 'secret='"

// Task 4: Generate file summary
"List all markdown files in /app and create a summary of what each file contains based on the first few lines"

// Task 5: Analyze package dependencies
"Read package.json in /app and list all production dependencies with their versions"
```

### 2. Codebase Analyzer (Webhook API)

**Workflow**: Claude Agent SDK - Codebase Analyzer

**How to test**:
1. Activate the workflow in n8n
2. Use curl to send POST requests
3. Check the response

**Basic Test**:
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "List all files in /tmp and describe what you find",
    "repository_path": "/tmp",
    "allowed_tools": ["Read", "Bash", "Glob"]
  }'
```

**Advanced Test Scenarios**:

#### Test 1: Find TODO Comments
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find all TODO, FIXME, and HACK comments in the codebase. Group them by priority and file.",
    "repository_path": "/app",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'
```

#### Test 2: Security Audit
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Perform a security audit. Look for: 1) Hardcoded secrets, 2) Dangerous functions (eval, exec), 3) Unvalidated inputs. Provide a report with severity levels.",
    "repository_path": "/app/src",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'
```

#### Test 3: Code Quality Analysis
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyze code quality: 1) Find functions longer than 50 lines, 2) Identify files with high complexity, 3) Check for proper error handling",
    "repository_path": "/app",
    "allowed_tools": ["Read", "Glob", "Grep", "Bash"]
  }'
```

#### Test 4: Dependency Analysis
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Read package.json and analyze dependencies. Check if there are any outdated packages or known vulnerabilities. Suggest updates.",
    "repository_path": "/app",
    "allowed_tools": ["Read", "Bash"]
  }'
```

#### Test 5: Test Coverage Check
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Compare source files in /src with test files in /tests. Identify which modules are missing test coverage.",
    "repository_path": "/app",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'
```

#### Test 6: Documentation Check
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Check if all public functions have JSDoc/docstring comments. List functions that are missing documentation.",
    "repository_path": "/app",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'
```

#### Test 7: API Endpoint Discovery
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find all API endpoints defined in the codebase. Look for Express routes, Flask routes, or similar patterns. Create a list with HTTP method, path, and handler function.",
    "repository_path": "/app",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'
```

#### Test 8: Environment Variables Audit
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find all environment variables used in the code (process.env.*, os.getenv, etc.). Check if they are documented in .env.example or README.",
    "repository_path": "/app",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'
```

## Understanding Agent Responses

### Success Response Format
```json
{
  "success": true,
  "analysis": "Detailed multi-step analysis from the agent...",
  "metadata": {
    "messages_count": 15,
    "task": "Original task description",
    "repository": "/app",
    "timestamp": "2025-12-14T20:30:00.000Z"
  }
}
```

### Error Response Format
```json
{
  "success": false,
  "error": "Error message describing what went wrong",
  "task": "Original task description"
}
```

## What Makes Agent SDK Different?

### Regular Claude API (Text Processor)
- **Single API call**: Send prompt → Get response
- **No tool usage**: Cannot read files or execute commands
- **Stateless**: Each request is independent
- **Use for**: Text summarization, Q&A, content generation

### Claude Agent SDK
- **Multi-step execution**: Agent makes multiple decisions
- **Tool usage**: Can read files, run bash, search code
- **Autonomous**: Agent decides which tools to use
- **Iterative**: Agent can refine its approach based on results
- **Use for**: Code analysis, file operations, system tasks

## Example: What the Agent Does Internally

When you send this task:
```bash
"Find all TODO comments in Python files"
```

**The agent autonomously:**
1. Uses **Glob** to find all `*.py` files
2. Uses **Grep** to search for "TODO" in those files
3. Uses **Read** to get context around each TODO
4. Analyzes and organizes the findings
5. Returns a structured report

**You see the final result**, but the agent made multiple tool calls to accomplish the task!

## Monitoring Agent Execution

### In n8n UI

1. Open the workflow
2. Click **"Executions"** in the left sidebar
3. View detailed execution logs
4. See which tools the agent used
5. Check token usage and timing

### Via Logs

If running n8n in Docker:
```bash
docker logs n8n-n8n-1 -f
```

Look for agent execution details in the logs.

## Performance Tips

### 1. Be Specific in Tasks
✅ **Good**: "Find TODO comments in JavaScript files in /src/components and list with file:line format"

❌ **Bad**: "Check the code"

### 2. Limit Tool Access
Only give tools the agent needs:
```json
{
  "allowed_tools": ["Read", "Glob"]  // Read-only access
}
```

Avoid giving unnecessary tools:
```json
{
  "allowed_tools": ["Read", "Write", "Edit", "Bash"]  // Too broad
}
```

### 3. Set Appropriate Repository Path
```json
{
  "repository_path": "/app/src"  // Specific directory
}
```

Not:
```json
{
  "repository_path": "/"  // Too broad, slow
}
```

### 4. Structure Your Requests
Ask for structured output:
```
"Find all TODOs and return as JSON with format:
{
  'high_priority': [...],
  'medium_priority': [...],
  'low_priority': [...]
}"
```

## Common Issues & Solutions

### Issue: "claude-agent-sdk not installed"

**Solution**:
```bash
# Access your n8n container
docker exec -it n8n-n8n-1 /bin/sh

# Install SDK
npm install @anthropic-ai/claude-agent-sdk
# OR
pip install claude-agent-sdk
```

### Issue: "ANTHROPIC_API_KEY not found"

**Solution**:
Add to your n8n environment (docker-compose.yml):
```yaml
environment:
  - ANTHROPIC_API_KEY=sk-ant-api-your-key
```

Then restart:
```bash
docker restart n8n-n8n-1
```

### Issue: Agent times out

**Solution**:
- Reduce scope of analysis (smaller repository path)
- Be more specific in your task
- Increase max_iterations in the code node

### Issue: Permission denied

**Solution**:
Check that n8n has access to the repository path:
```bash
# In the workflow code, verify path exists
docker exec -it n8n-n8n-1 ls -la /app
```

## Integration Ideas

### 1. GitHub PR Review Bot
```
GitHub Webhook → n8n → Clone Repo → Agent Analyzes → Post Review
```

### 2. Scheduled Code Quality Report
```
Cron Trigger → Agent Audits Codebase → Generate Report → Email Team
```

### 3. CI/CD Integration
```
Build Complete → Agent Checks for Issues → Block/Allow Deploy
```

### 4. Documentation Generator
```
Manual Trigger → Agent Reads Code → Generate Docs → Commit to Repo
```

## Next Steps

1. **Start with simple tasks** using the manual trigger workflow
2. **Test webhook workflows** with curl commands
3. **Monitor executions** in n8n to see what the agent does
4. **Combine with other n8n nodes** (Slack, Email, Database, etc.)
5. **Build production workflows** based on your needs

## Resources

- [AGENT-SDK-GUIDE.md](./AGENT-SDK-GUIDE.md) - Complete setup guide
- [README.md](./README.md) - All workflows documentation
- [Claude Agent SDK Docs](https://platform.claude.com/docs/en/agent-sdk/overview.md)

---

**Ready to test?** Start with the simple examples above and explore from there!
