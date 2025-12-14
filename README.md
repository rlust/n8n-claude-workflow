# n8n + Claude Workflows

A collection of production-ready n8n workflows that integrate with Claude (Anthropic) for intelligent automation tasks, including both **Claude API** (simple text processing) and **Claude Agent SDK** (autonomous agents).

## Overview

This repository contains example workflows and comprehensive documentation to help you integrate Claude's AI capabilities into your n8n automation workflows. Whether you're building chatbots, automating code reviews, processing documents, or running autonomous agents that can execute code, these examples will get you started quickly.

## What's Included

### 🔧 Ready-to-Use Workflows

#### Claude API Workflows (Simple HTTP calls)

1. **Claude Text Processor** - Simple text processing with manual trigger
   - Text summarization
   - Content generation
   - Language translation
   - Question answering

2. **Claude Code Analyzer** - Webhook-based code analysis service
   - Automated code reviews
   - Security vulnerability detection
   - Performance optimization suggestions
   - Best practices recommendations

3. **Claude Document Summarizer** - Smart document summarization
   - Customizable summary length and format
   - Compression ratio tracking
   - Support for multiple formats (bullets/paragraphs)

#### Claude Agent SDK Workflows (Autonomous agents)

4. **Claude Agent SDK - Simple Task Runner** - JavaScript/TypeScript agent
   - Autonomous tool usage (Read, Bash, Glob, Grep)
   - Multi-step task execution
   - Perfect for one-off automation tasks

5. **Claude Agent SDK - Codebase Analyzer** - Advanced Python agent
   - Webhook-triggered autonomous analysis
   - Full codebase exploration and review
   - Structured JSON output
   - Ideal for CI/CD integration

### 📚 Documentation

- **[QUICKSTART.md](n8n-workflows/QUICKSTART.md)** - Get started in 5 minutes
- **[README.md](n8n-workflows/README.md)** - Comprehensive guide with examples
- **[AGENT-SDK-GUIDE.md](n8n-workflows/AGENT-SDK-GUIDE.md)** - Complete guide to Claude Agent SDK integration
- **Test Scripts** - Ready-to-use webhook testing tools

## Quick Start

### Prerequisites

- n8n instance running (local or cloud)
- Anthropic API key ([get one here](https://console.anthropic.com))

### Setup in 3 Steps

1. **Get Your API Key**
   ```bash
   # Visit https://console.anthropic.com
   # Create an API key (starts with sk-ant-api...)
   ```

2. **Configure n8n Credentials**
   - Open your n8n instance
   - Settings → Credentials → Add "HTTP Header Auth"
   - Header name: `x-api-key`
   - Value: Your Anthropic API key

3. **Import Workflows**
   - Download workflows from `n8n-workflows/examples/`
   - In n8n: Workflows → Import from File
   - Select a workflow JSON file
   - Configure credentials and test!

## Example Usage

### Code Analysis Webhook

After importing and activating the code analyzer workflow:

```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "function calculateTotal(items) {
      let total = 0;
      for(let i = 0; i < items.length; i++) {
        total += items[i].price;
      }
      return total;
    }",
    "language": "javascript"
  }'
```

Response:
```json
{
  "success": true,
  "analysis": "### Code Quality Assessment\n1. **Functionality**: The function works correctly...",
  "metadata": {
    "model": "claude-sonnet-4-5-20250929",
    "tokens": 847,
    "timestamp": "2025-12-14T..."
  }
}
```

### Document Summarization

```bash
curl -X POST http://100.82.85.95:5678/webhook/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Long document text here...",
    "format": "bullets",
    "max_length": "short"
  }'
```

### Autonomous Agent (Agent SDK)

After setting up the Agent SDK workflow (see [AGENT-SDK-GUIDE.md](n8n-workflows/AGENT-SDK-GUIDE.md)):

```bash
curl -X POST http://100.82.85.95:5678/webhook/analyze-codebase \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find all TODO comments in the codebase and create a summary report",
    "repository_path": "/path/to/repo",
    "allowed_tools": ["Read", "Glob", "Grep"]
  }'
```

Response:
```json
{
  "success": true,
  "analysis": "I found 23 TODO comments across 12 files:\n\n**High Priority:**\n- src/auth.js:45 - TODO: Add rate limiting\n- src/api.js:128 - TODO: Implement error handling\n\n**Medium Priority:**\n...",
  "metadata": {
    "messages_count": 15,
    "task": "Find all TODO comments...",
    "timestamp": "2025-12-14T..."
  }
}
```

**What's different?** The agent autonomously:
1. Used Glob to find all code files
2. Used Grep to search for TODO comments
3. Read relevant files for context
4. Organized findings by priority
5. Generated a structured report

## Available Claude Models

| Model | Use Case | Speed | Cost |
|-------|----------|-------|------|
| `claude-sonnet-4-5-20250929` | Balanced performance (recommended) | Fast | Medium |
| `claude-opus-4-5-20251101` | Most capable, complex tasks | Slower | Higher |
| `claude-haiku-3-5-20241022` | Simple tasks, high volume | Fastest | Lowest |

## Use Cases

### Business Automation
- Email response generation
- Customer inquiry routing
- Document processing and categorization
- Meeting notes summarization

### Development Workflows
- Automated code reviews
- Documentation generation
- Bug report analysis
- Test case generation

### Content Creation
- Blog post drafting
- Social media content generation
- Product description writing
- Translation and localization

### Data Processing
- Text extraction and transformation
- Sentiment analysis
- Data classification
- Report generation

## Project Structure

```
n8n-claude-workflow/
├── README.md                          # This file
└── n8n-workflows/
    ├── QUICKSTART.md                  # 5-minute setup guide
    ├── README.md                      # Detailed documentation
    ├── test-webhook.sh                # Testing utilities
    ├── examples/
    │   ├── claude-text-processor.json
    │   ├── claude-code-analyzer.json
    │   └── claude-document-summarizer.json
    └── templates/                      # Additional templates (coming soon)
```

## Advanced Features

### Custom Prompts
All workflows can be customized by modifying the prompt construction nodes:

```javascript
// Example: Custom prompt for specific use case
const prompt = `Analyze this ${language} code for:
- Security vulnerabilities
- Performance issues
- Code style compliance with ${styleGuide}

Code:
${code}`;
```

### Error Handling
Workflows include built-in error handling for:
- API rate limits
- Invalid inputs
- Timeout management
- Response validation

### Integration Patterns
Combine Claude workflows with other n8n nodes:
- **Slack** - Build AI chatbots
- **Gmail** - Automated email responses
- **Google Sheets** - Data analysis and enrichment
- **Webhooks** - REST API integrations
- **Databases** - Intelligent data processing

## Tips & Best Practices

### 1. Token Management
- Monitor usage via response metadata
- Set appropriate `max_tokens` limits
- Use Claude Haiku for simple tasks to reduce costs

### 2. Prompt Engineering
- Be specific and provide context
- Use examples in your prompts
- Break complex tasks into steps
- Test and iterate on prompts

### 3. Security
- Never hardcode API keys
- Use n8n's credential system
- Validate webhook inputs
- Sanitize data before sending to Claude

### 4. Performance
- Implement caching for repeated queries
- Use queues for high-volume workflows
- Set appropriate timeouts
- Monitor execution logs

## Troubleshooting

### Common Issues

**401 Unauthorized**
- Verify API key is correct
- Check header name is exactly `x-api-key`
- Ensure credential is selected in HTTP Request node

**Workflow Not Triggering**
- Confirm workflow is activated
- Check webhook URL is correct
- Review n8n execution logs

**Unexpected Responses**
- Review the exact prompt being sent
- Verify you're using the correct model
- Check response parsing logic

## Contributing

Contributions are welcome! Feel free to:
- Submit new workflow examples
- Improve documentation
- Report issues
- Suggest features

## Resources

- **[Anthropic API Documentation](https://docs.anthropic.com)** - Official API docs
- **[n8n Documentation](https://docs.n8n.io)** - n8n platform docs
- **[Claude Pricing](https://www.anthropic.com/pricing)** - API pricing details
- **[n8n Community](https://community.n8n.io)** - Community support

## Cost Estimation

Typical costs using Claude Sonnet 4.5:

| Operation | Tokens | Cost (approx) |
|-----------|--------|---------------|
| Simple text processing | ~500 | $0.0015 |
| Code review (medium) | ~2,000 | $0.006 |
| Document summarization | ~1,500 | $0.0045 |
| Complex analysis | ~4,000 | $0.012 |

*Prices are approximate and based on current Anthropic pricing. Check [official pricing](https://www.anthropic.com/pricing) for exact rates.*

## License

MIT License - Feel free to use these workflows in your projects.

## Support

- **Issues**: Open an issue in this repository
- **Questions**: Check the [documentation](n8n-workflows/README.md)
- **Updates**: Watch this repo for new workflows and features

## Changelog

### 2025-12-14 - Initial Release
- ✨ Added 3 example workflows
- 📚 Comprehensive documentation
- 🧪 Test scripts and examples
- 🚀 Quick start guide

---

Made with ❤️ using [Claude Code](https://claude.com/claude-code) and [n8n](https://n8n.io)
