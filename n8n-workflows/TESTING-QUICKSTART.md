# Testing Quick Start Guide

Fast reference for running automated tests on n8n Claude workflows.

## ⚡ Quick Commands

```bash
# Install dependencies (first time only)
make install
# OR
pip install -r tests/requirements.txt

# Run all tests
make test

# Run fast tests only (skip slow agent tests)
make test-fast

# Run with coverage report
make test-coverage

# Generate HTML test report
make test-html
```

## 📊 What Gets Tested

✅ **Code Analyzer** - Code analysis workflow
✅ **Document Summarizer** - Document summarization
✅ **Agent Workflows** - Autonomous agent tasks
✅ **Performance** - Response times and concurrency
✅ **Error Handling** - Invalid inputs and edge cases

## 🎯 Common Test Scenarios

### Test Specific Workflow

```bash
# Test only code analyzer
pytest tests/test_workflows.py::TestCodeAnalyzer -v

# Test only document summarizer
pytest tests/test_workflows.py::TestDocumentSummarizer -v

# Test only agent workflows
pytest tests/test_workflows.py::TestAgentCodebaseAnalyzer -v
```

### Test by Category

```bash
# Skip slow tests (good for quick checks)
pytest tests/ -m "not slow" -v

# Run only performance tests
pytest tests/ -m "performance" -v

# Run only agent tests
pytest tests/ -m "agent" -v
```

### Debugging

```bash
# Stop at first failure
pytest tests/ -x -v

# Show print statements
pytest tests/ -s -v

# Full debug mode
make test-debug
```

## ✅ Validation Features

Each test automatically validates:
- ✓ HTTP status codes
- ✓ Response structure (required fields)
- ✓ Success/failure status
- ✓ Metadata completeness
- ✓ Response content quality
- ✓ Performance metrics

## 📈 Test Results

After running tests:

```bash
# View coverage report
open htmlcov/index.html

# View HTML test report
open test-results/report.html
```

## 🔧 Configuration

Set environment variables if needed:

```bash
# Custom n8n URL
export N8N_BASE_URL="http://your-n8n-instance:5678"

# Custom timeout
export TEST_TIMEOUT=60

# Then run tests
make test
```

## 🚀 CI/CD

Tests run automatically on:
- Push to main/develop
- Pull requests
- Daily at 2 AM UTC
- Manual trigger in GitHub Actions

## 📝 Test Structure

```
✓ 12+ test cases covering:
  ├─ Basic functionality
  ├─ Error handling
  ├─ Multiple languages/formats
  ├─ Input validation
  ├─ Performance SLA
  └─ Concurrent requests
```

## 🎓 Examples

### Example Test Output

```
tests/test_workflows.py::TestCodeAnalyzer::test_basic_code_analysis PASSED [8%]
✓ Test completed in 1245.67ms

tests/test_workflows.py::TestCodeAnalyzer::test_code_analysis_with_issues PASSED [16%]
tests/test_workflows.py::TestDocumentSummarizer::test_basic_summarization PASSED [25%]
✓ Summarized in 1567.89ms
```

### Example Coverage Report

```
Name                    Stmts   Miss  Cover
-------------------------------------------
test_workflows.py        245     12    95%
conftest.py               28      2    93%
-------------------------------------------
TOTAL                    273     14    95%
```

## 🆘 Troubleshooting

### n8n not responding?
```bash
curl http://100.82.85.95:5678/healthz
```

### Tests timing out?
```bash
export TEST_TIMEOUT=60
make test
```

### Module not found?
```bash
make install
```

## 📚 Full Documentation

For detailed information, see:
- `tests/README.md` - Complete testing guide
- `pytest.ini` - Test configuration
- `.github/workflows/test-workflows.yml` - CI/CD setup

---

**Need help?** Run `make help` for all available commands.
