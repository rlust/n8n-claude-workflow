# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📌 Recent Work

### Session: 2025-12-17 - Scheduled Stock Analysis Workflow
**IMPORTANT:** Read **SESSION-SUMMARY-2025-12-17.md** for complete session details

**What was done:**
- ✅ Fixed and enhanced smart_calc.py (interactive calculator with Claude Agent SDK)
- ✅ Created working stock-to-telegram workflow (v3)
- ✅ Added scheduled automation (Cron trigger at 9:30 AM weekdays)
- ✅ Integrated Telegram bot for notifications
- ✅ Dual trigger support (webhook + cron)
- ✅ All credentials stored in .env file
- ✅ Changes pushed to GitHub (commit: 2a4f7f0)

**Active Workflows:**
- Stock to Telegram v3 (Scheduled) - ID: B96iHmEjsX6Yo3IM
- Analyzes AAPL, MSFT at 9:30 AM Mon-Fri
- Also available via webhook for on-demand requests

### Session: 2025-12-15 - Testing Infrastructure
**Read:** n8n-workflows/SESSION-HISTORY.md

**What was done:**
- ✅ Implemented comprehensive automated testing suite with pytest
- ✅ Added 12+ test cases with assertions and validation
- ✅ Created GitHub Actions CI/CD workflow
- ✅ Added ResponseValidator and PerformanceTracker helper classes
- ✅ Created 17 files (3,000+ lines)
- ✅ All changes pushed to GitHub (commit: dcfcd82)

## 🔐 Credentials and Configuration

**IMPORTANT:** All API keys and credentials are stored in `.env` file (not in Git)

### Available Credentials in .env:
- `N8N_URL` - n8n instance URL
- `N8N_API_KEY` - n8n API authentication key
- `ANTHROPIC_API_KEY` - Claude API key
- `ANTHROPIC_MODEL` - Claude model ID
- `TELEGRAM_BOT_TOKEN` - Telegram bot token
- `TELEGRAM_CHAT_ID` - Telegram chat ID
- `WORKFLOW_ID_STOCK_TO_TELEGRAM_V3` - Main workflow ID
- `WEBHOOK_URL_STOCK_TELEGRAM_V3` - Webhook endpoint

### Usage in Scripts:
```bash
# Load environment variables
source .env

# Or use in Python
from dotenv import load_dotenv
load_dotenv()

# Or export for shell scripts
export N8N_API_KEY=$(grep N8N_API_KEY .env | cut -d '=' -f2)
```

### For Future Sessions:
When resuming work, Claude Code should read the `.env` file to access all necessary credentials and configuration.

## Development Commands

### Test (n8n-workflows/)
```bash
cd n8n-workflows

# Install test dependencies (first time only)
make install

# Run fast tests (skip slow agent tests)
make test-fast

# Run all tests
make test

# Run with coverage report
make test-coverage

# Run with HTML report
make test-html

# Run specific test
pytest tests/test_workflows.py::TestCodeAnalyzer -v

# Run in debug mode
make test-debug
```

### Lint
```bash
cd n8n-workflows
make lint
```

### Clean
```bash
cd n8n-workflows
make clean
```

## Architecture Overview

### Repository Structure
```
/root/claude/
├── CLAUDE.md                        # This file
├── README.md                        # Main repository README
└── n8n-workflows/                   # n8n workflow testing project
    ├── examples/                    # 5 n8n workflow JSON files
    ├── tests/                       # Automated test suite
    │   ├── test_workflows.py       # Main test file (12+ tests)
    │   ├── conftest.py             # Shared fixtures
    │   ├── requirements.txt        # Python dependencies
    │   └── README.md               # Testing documentation
    ├── .github/workflows/          # CI/CD configuration
    ├── pytest.ini                  # pytest configuration
    ├── Makefile                    # Build commands
    ├── SESSION-HISTORY.md          # Complete session log
    ├── IMPLEMENTATION-SUMMARY.md   # Project summary
    ├── TESTING-STATUS.md           # Current status
    └── TESTING-QUICKSTART.md       # Quick reference
```

### n8n Workflows (5 total)
1. **claude-text-processor.json** - Simple text processing
2. **claude-code-analyzer.json** - Code analysis via webhook
3. **claude-document-summarizer.json** - Document summarization
4. **claude-agent-sdk-simple.json** - Simple agent (JavaScript)
5. **claude-agent-sdk-codebase-analyzer.json** - Advanced agent (Python)

### Testing Architecture
- **Framework:** pytest 9.0.2
- **Helper Classes:**
  - `ResponseValidator` - Validates API responses
  - `PerformanceTracker` - Tracks execution time and SLA
  - `TestConfig` - Centralized configuration
- **Test Markers:** slow, integration, performance, agent, api
- **CI/CD:** GitHub Actions with multi-version Python testing

## Key Conventions

### Test Organization
- Tests are grouped by workflow type (TestCodeAnalyzer, TestDocumentSummarizer, etc.)
- Use markers to categorize tests: `@pytest.mark.slow`, `@pytest.mark.integration`
- All tests use validators and performance trackers
- Fixtures in `conftest.py` for shared test data

### Naming Conventions
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Helper functions: descriptive names with underscores

### Documentation
- All test files have docstrings
- Each test function has a description
- README files provide comprehensive guides
- Examples included in documentation

### Git Workflow
- GitHub CLI (`gh`) configured for authentication
- Commit messages follow conventional format
- All commits include Claude Code attribution
- Branch: master
- Remote: https://github.com/rlust/n8n-claude-workflow

## Quick Reference

### To Resume Previous Session
```bash
# Read the session history
cat n8n-workflows/SESSION-HISTORY.md

# Check current status
cat n8n-workflows/TESTING-STATUS.md

# Run tests
cd n8n-workflows && make test-fast
```

### Common Tasks
```bash
# Run tests
cd n8n-workflows && make test-fast

# View test documentation
cat n8n-workflows/tests/README.md

# Check test status
cat n8n-workflows/TESTING-STATUS.md

# Push to GitHub
git add . && git commit -m "message" && git push origin master
```

### Next Steps (User Action Required)
1. Activate n8n workflows at http://100.82.85.95:5678
2. Configure Anthropic API credentials in n8n
3. Run: `make test-fast` to verify
4. Provide Telegram bot credentials for notifications

## Helpful Tips

- **Session Context:** Always read SESSION-HISTORY.md first to understand what was done
- **Test Status:** Check TESTING-STATUS.md for current state and next steps
- **Quick Commands:** Use Makefile commands (make test-fast, make test-coverage, etc.)
- **Documentation:** Comprehensive guides in tests/README.md and TESTING-QUICKSTART.md
