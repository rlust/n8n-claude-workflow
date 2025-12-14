# n8n + Claude Integration

This directory contains example n8n workflows that integrate with Claude for intelligent automation tasks, including both **Claude API** (simple text processing) and **Claude Agent SDK** (autonomous agents that can execute code).

## Prerequisites

- n8n running (you already have this on port 5678)
- Anthropic API key (get one from https://console.anthropic.com)

## Setup Instructions

### 1. Configure Anthropic API Credentials in n8n

1. Access your n8n instance at http://100.82.85.95:5678
2. Go to **Settings** → **Credentials** → **New**
3. Search for **HTTP Header Auth** (or use the HTTP Request node with custom headers)
4. Create a credential with:
   - **Name**: Anthropic API Key
   - **Name** field: `x-api-key`
   - **Value** field: Your Anthropic API key

### 2. Import Workflows

1. In n8n, click **Workflows** → **Import from File**
2. Import the workflow JSON files from the `examples/` directory:

   **Claude API Workflows** (Simple HTTP calls):
   - `claude-text-processor.json` - Simple text processing with Claude
   - `claude-code-analyzer.json` - Code analysis via webhook
   - `claude-document-summarizer.json` - Document summarization service

   **Claude Agent SDK Workflows** (Autonomous agents):
   - `claude-agent-sdk-simple.json` - Simple agent task runner (JavaScript)
   - `claude-agent-sdk-codebase-analyzer.json` - Advanced codebase analysis (Python)

### 3. Configure Each Workflow

After importing, update each workflow:

1. Open the workflow
2. Click on the **Call Claude API** node
3. Under **Authentication**, select your Anthropic API Key credential
4. Save the workflow

## Available Workflows

### 1. Claude Text Processor

**File**: `examples/claude-text-processor.json`

**Purpose**: Simple text processing using Claude API

**How to use**:
1. Import the workflow
2. Configure the API credentials
3. Modify the "Set Input Text" node to change the prompt
4. Click "Test workflow" to run

**Use cases**:
- Text summarization
- Content generation
- Language translation
- Question answering

### 2. Claude Code Analyzer

**File**: `examples/claude-code-analyzer.json`

**Purpose**: Webhook-based code analysis service

**How to use**:
1. Import and activate the workflow
2. Get the webhook URL from the workflow (click on the webhook node)
3. Send POST requests to analyze code

**Example request**:
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-code \\
  -H "Content-Type: application/json" \\
  -d '{
    "code": "function hello() { console.log(\"Hello\"); }",
    "language": "javascript",
    "analysis_type": "review"
  }'
```

**Response**:
```json
{
  "success": true,
  "analysis": "Detailed code analysis from Claude...",
  "metadata": {
    "model": "claude-sonnet-4-5-20250929",
    "tokens": 1234,
    "timestamp": "2025-12-14T..."
  }
}
```

### 3. Claude Document Summarizer

**File**: `examples/claude-document-summarizer.json`

**Purpose**: Webhook-based document summarization service with customizable output

**How to use**:
1. Import and activate the workflow
2. Get the webhook URL from the workflow
3. Send POST requests with text to summarize

**Example request**:
```bash
curl -X POST http://100.82.85.95:5678/webhook/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long document text here...",
    "format": "bullets",
    "max_length": "short"
  }'
```

**Parameters**:
- `text` (required): The text to summarize
- `format` (optional): "paragraph" or "bullets" (default: "paragraph")
- `max_length` (optional): "short", "medium", or "long" (default: "medium")

**Response**:
```json
{
  "success": true,
  "summary": "Summarized content...",
  "metadata": {
    "original_length": 5000,
    "summary_length": 500,
    "compression_ratio": "90%"
  }
}
```

### 4. Claude Agent SDK - Simple Task Runner

**File**: `examples/claude-agent-sdk-simple.json`

**Purpose**: Demonstrates autonomous agent execution using Claude Agent SDK (JavaScript/TypeScript)

**What makes this different**: Unlike the simple API workflows above, this uses the **Claude Agent SDK** which allows Claude to autonomously use tools (read files, run commands, search code) to accomplish tasks.

**How to use**:
1. Install the SDK in your n8n environment: `npm install @anthropic-ai/claude-agent-sdk`
2. Set environment variable: `ANTHROPIC_API_KEY=your_key`
3. Import and run the workflow
4. Modify the task in the "Set Task" node

**Example tasks**:
- "Find all TODO comments in Python files and list them"
- "Analyze test coverage by comparing test files to source files"
- "Generate a summary of all API endpoints in this codebase"

### 5. Claude Agent SDK - Codebase Analyzer

**File**: `examples/claude-agent-sdk-codebase-analyzer.json`

**Purpose**: Advanced webhook-based codebase analysis using Claude Agent SDK (Python)

**Capabilities**:
- Autonomous file exploration and analysis
- Multi-step reasoning and tool usage
- Structured JSON output
- Customizable tool permissions

**How to use**:
1. Install the SDK: `pip install claude-agent-sdk`
2. Set `ANTHROPIC_API_KEY` environment variable
3. Import and activate the workflow
4. Send POST requests with analysis tasks

**Example request**:
```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Review all JavaScript files for security issues",
    "repository_path": "/path/to/repo",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'
```

**Response**:
```json
{
  "success": true,
  "analysis": "Detailed analysis from Claude agent...",
  "metadata": {
    "messages_count": 15,
    "task": "Review all JavaScript files...",
    "timestamp": "2025-12-14T..."
  }
}
```

**For complete setup guide, see**: [AGENT-SDK-GUIDE.md](AGENT-SDK-GUIDE.md)

## Advanced Usage

### Creating Custom Workflows

You can create custom workflows by:

1. Using the **HTTP Request** node to call Claude API
2. Setting these parameters:
   - **Method**: POST
   - **URL**: `https://api.anthropic.com/v1/messages`
   - **Headers**:
     - `x-api-key`: Your API key
     - `anthropic-version`: `2023-06-01`
     - `content-type`: `application/json`
   - **Body**:
     ```json
     {
       "model": "claude-sonnet-4-5-20250929",
       "max_tokens": 1024,
       "messages": [
         {"role": "user", "content": "Your prompt here"}
       ]
     }
     ```

### Available Claude Models

- `claude-sonnet-4-5-20250929` - Latest Sonnet (balanced performance/cost)
- `claude-opus-4-5-20251101` - Most capable model
- `claude-haiku-3-5-20241022` - Fastest, most cost-effective

### Common Integration Patterns

1. **Email Automation**: Receive emails → Claude processes/categorizes → Send responses
2. **Slack Bot**: Slack trigger → Claude answers questions → Post to Slack
3. **Data Processing**: Load data → Claude analyzes/transforms → Save results
4. **Content Generation**: Schedule trigger → Claude generates content → Post to CMS
5. **Code Review Bot**: GitHub webhook → Claude reviews code → Comment on PR

## Workflow Templates

Additional workflow templates are available in the `templates/` directory:

- Coming soon: Document summarizer
- Coming soon: Email responder
- Coming soon: Social media content generator
- Coming soon: Data extractor and analyzer

## Tips and Best Practices

### 1. Token Management
- Monitor token usage in responses (`usage.input_tokens` + `usage.output_tokens`)
- Set appropriate `max_tokens` limits
- Use Claude Haiku for simple tasks to reduce costs

### 2. Error Handling
- Add error catching nodes to handle API failures
- Implement retry logic for transient errors
- Log failures for debugging

### 3. Rate Limiting
- Anthropic API has rate limits based on your plan
- Implement queuing for high-volume workflows
- Use the Wait node to pace requests

### 4. Prompt Engineering
- Be specific and clear in your prompts
- Provide context and examples
- Use system messages for consistent behavior
- Break complex tasks into smaller steps

### 5. Security
- Never hardcode API keys in workflows
- Use n8n's credential system
- Validate webhook inputs
- Sanitize data before sending to Claude

## Testing Workflows

### Quick Test
1. Use the manual trigger node
2. Set test data in Set nodes
3. Execute and check results

### Webhook Testing
```bash
# Test the code analyzer
curl -X POST http://100.82.85.95:5678/webhook/analyze-code \\
  -H "Content-Type: application/json" \\
  -d '{
    "code": "const x = 1; var y = 2;",
    "language": "javascript"
  }'
```

## Troubleshooting

### API Authentication Errors
- Verify your API key in n8n credentials
- Check the header name is exactly `x-api-key`
- Ensure `anthropic-version` header is set

### Workflow Not Triggering
- Check if workflow is activated
- Verify webhook URLs are correct
- Check n8n logs for errors

### Unexpected Responses
- Review the prompt being sent to Claude
- Check if you're using the correct model
- Verify the response parsing logic

## Resources

- [Anthropic API Documentation](https://docs.anthropic.com)
- [n8n Documentation](https://docs.n8n.io)
- [Claude API Pricing](https://www.anthropic.com/pricing)
- [n8n Community](https://community.n8n.io)

## Support

For issues or questions:
1. Check n8n execution logs
2. Review Claude API response errors
3. Test API calls independently with curl
4. Consult n8n community forums

## Next Steps

1. Import and test the example workflows
2. Modify prompts to fit your use case
3. Create custom workflows for your automation needs
4. Explore combining Claude with other n8n nodes (databases, APIs, etc.)
