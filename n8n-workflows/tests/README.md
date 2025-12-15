# Automated Testing for n8n Claude Workflows

Comprehensive automated test suite for validating n8n workflows with proper assertions, performance tracking, and CI/CD integration.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [CI/CD Integration](#cicd-integration)
- [Writing New Tests](#writing-new-tests)
- [Troubleshooting](#troubleshooting)

## Overview

This test suite provides:
- **Automated validation** with proper assertions
- **Response structure validation** for all workflows
- **Performance tracking** and metrics
- **Concurrent request testing**
- **Error handling validation**
- **CI/CD ready** with GitHub Actions

### Test Coverage

The suite tests all 5 n8n workflows:
1. ✅ Claude Text Processor
2. ✅ Claude Code Analyzer
3. ✅ Claude Document Summarizer
4. ✅ Claude Agent SDK Simple Task Runner
5. ✅ Claude Agent SDK Codebase Analyzer

## Quick Start

### 1. Install Dependencies

```bash
cd /root/claude/n8n-workflows
pip install -r tests/requirements.txt
```

### 2. Run All Tests

```bash
pytest tests/ -v
```

### 3. Run Fast Tests Only (Skip Slow Agent Tests)

```bash
pytest tests/ -m "not slow" -v
```

### 4. Run Specific Test Class

```bash
pytest tests/test_workflows.py::TestCodeAnalyzer -v
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── test_workflows.py        # Main test suite
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Key Components

#### ResponseValidator
Validates API response structure and content:
- `validate_structure()` - Checks required fields exist
- `validate_success()` - Verifies success status
- `validate_metadata()` - Validates metadata structure
- `validate_non_empty()` - Ensures fields have content

#### PerformanceTracker
Tracks and validates performance metrics:
- `start()` / `stop()` - Time operations
- `duration_ms` - Get duration in milliseconds
- `assert_within_timeout()` - Validate performance SLA

#### TestConfig
Centralized configuration:
- Base URL for n8n instance
- Endpoint definitions
- Timeout settings

## Running Tests

### Basic Usage

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=tests --cov-report=html

# Run with detailed output
pytest tests/ -vv --tb=long

# Run and stop at first failure
pytest tests/ -x

# Run with parallel execution (faster)
pytest tests/ -n auto
```

### Filter by Markers

```bash
# Run only integration tests
pytest tests/ -m integration

# Run only performance tests
pytest tests/ -m performance

# Run only agent tests
pytest tests/ -m agent

# Exclude slow tests
pytest tests/ -m "not slow"

# Run only API tests (non-agent)
pytest tests/ -m "api and not agent"
```

### Filter by Test Name

```bash
# Run specific test
pytest tests/test_workflows.py::TestCodeAnalyzer::test_basic_code_analysis

# Run all code analyzer tests
pytest tests/test_workflows.py::TestCodeAnalyzer

# Run tests matching pattern
pytest tests/ -k "code_analysis"
```

### Generate Reports

```bash
# HTML report
pytest tests/ --html=report.html --self-contained-html

# JUnit XML (for CI/CD)
pytest tests/ --junit-xml=results.xml

# JSON report
pytest tests/ --json-report --json-report-file=report.json
```

## Test Categories

### 1. Code Analyzer Tests (`TestCodeAnalyzer`)

Tests the code analysis workflow with various inputs:

- `test_basic_code_analysis` - Validates basic functionality
- `test_code_analysis_with_issues` - Tests detection of code issues
- `test_multiple_languages` - Tests Python, JavaScript, Java support
- `test_empty_code_handling` - Tests error handling

**Example:**
```bash
pytest tests/test_workflows.py::TestCodeAnalyzer -v
```

### 2. Document Summarizer Tests (`TestDocumentSummarizer`)

Tests document summarization with different options:

- `test_basic_summarization` - Tests basic summarization
- `test_bullet_format` - Tests bullet point output
- `test_input_validation` - Tests minimum length validation
- `test_different_lengths` - Tests short/medium/long outputs

**Example:**
```bash
pytest tests/test_workflows.py::TestDocumentSummarizer -v
```

### 3. Agent Tests (`TestAgentCodebaseAnalyzer`)

Tests autonomous agent workflows (marked as `slow`):

- `test_basic_agent_analysis` - Tests basic agent task
- `test_agent_file_search` - Tests file search capabilities
- `test_agent_error_handling` - Tests error handling

**Example:**
```bash
# Include slow tests
pytest tests/test_workflows.py::TestAgentCodebaseAnalyzer -v

# Skip in quick runs
pytest tests/ -m "not slow"
```

### 4. Performance Tests (`TestPerformance`)

Tests performance and concurrency:

- `test_response_time_acceptable` - Validates SLA compliance
- `test_concurrent_requests` - Tests parallel request handling

**Example:**
```bash
pytest tests/test_workflows.py::TestPerformance -v
```

## CI/CD Integration

### GitHub Actions

Automated tests run on:
- **Push** to main/develop branches
- **Pull requests** to main/develop
- **Daily schedule** (2 AM UTC)
- **Manual trigger** via workflow_dispatch

#### Workflow Features

1. **Multi-version testing** - Python 3.9, 3.10, 3.11
2. **Fast PR tests** - Excludes slow tests on PRs
3. **Coverage reporting** - Uploads to Codecov
4. **Test artifacts** - HTML reports and coverage
5. **Performance tests** - Separate scheduled job

#### View Results

1. Go to GitHub Actions tab
2. Select "Test n8n Workflows" workflow
3. Download test artifacts for detailed reports

### Local CI Simulation

```bash
# Run tests exactly as CI does
pytest tests/ \
  --verbose \
  --tb=short \
  --cov=tests \
  --cov-report=xml \
  --cov-report=html \
  --junit-xml=test-results/junit.xml \
  --html=test-results/report.html
```

## Writing New Tests

### Test Template

```python
def test_new_feature(self, validator, perf_tracker):
    """Test description."""
    perf_tracker.start()

    # Make API request
    response = requests.post(
        TestConfig.ENDPOINT,
        json={"param": "value"},
        timeout=TestConfig.TIMEOUT
    )

    perf_tracker.stop()

    # Assert HTTP status
    assert response.status_code == 200

    # Parse response
    data = response.json()

    # Validate structure
    validator.validate_structure(data, ["success", "result"])
    validator.validate_success(data)

    # Custom assertions
    assert data["result"] == "expected", "Result mismatch"

    # Performance validation
    perf_tracker.assert_within_timeout(5000)  # 5 seconds

    print(f"✓ Test completed in {perf_tracker.duration_ms:.2f}ms")
```

### Adding Markers

```python
import pytest

@pytest.mark.slow
@pytest.mark.integration
def test_complex_workflow(self):
    """Test that takes a long time."""
    pass
```

### Using Fixtures

```python
def test_with_fixtures(self, sample_code, sample_document):
    """Use predefined fixtures from conftest.py."""
    code = sample_code["python"]
    doc = sample_document
    # Test logic here
```

## Configuration

### Environment Variables

Set these to customize test behavior:

```bash
# n8n instance URL
export N8N_BASE_URL="http://100.82.85.95:5678"

# Test timeout in seconds
export TEST_TIMEOUT=30
```

### pytest.ini

Configuration file controls:
- Test discovery patterns
- Output formatting
- Default markers
- Timeout settings

## Troubleshooting

### Common Issues

#### 1. Connection Refused

```
requests.exceptions.ConnectionError: Connection refused
```

**Solution:** Ensure n8n is running:
```bash
# Check if n8n is accessible
curl http://100.82.85.95:5678/healthz
```

#### 2. Tests Timeout

```
pytest.TimeoutError: test exceeded timeout
```

**Solution:** Increase timeout for slow tests:
```bash
export TEST_TIMEOUT=60
pytest tests/ -v
```

#### 3. Import Errors

```
ModuleNotFoundError: No module named 'pytest'
```

**Solution:** Install dependencies:
```bash
pip install -r tests/requirements.txt
```

#### 4. n8n Workflows Not Active

**Solution:** Activate workflows in n8n UI or check webhook URLs

### Debug Mode

Run tests with extra debugging:

```bash
# Show all print statements
pytest tests/ -v -s

# Show full traceback
pytest tests/ -v --tb=long

# Show local variables in traceback
pytest tests/ -v --tb=long --showlocals

# Drop into debugger on failure
pytest tests/ -v --pdb
```

### Performance Issues

If tests are slow:

```bash
# Run in parallel (4 workers)
pytest tests/ -n 4

# Skip slow tests
pytest tests/ -m "not slow"

# Profile test execution
pytest tests/ --durations=10
```

## Best Practices

1. **Always use validators** - Don't write manual assertions for common validations
2. **Track performance** - Use PerformanceTracker for timing-sensitive tests
3. **Mark appropriately** - Use markers (slow, integration, etc.) for filtering
4. **Descriptive test names** - Use `test_feature_scenario_expected` pattern
5. **Clean up** - Use fixtures for setup/teardown
6. **Independent tests** - Tests should not depend on each other
7. **Meaningful assertions** - Include context in assertion messages

## Examples

### Example 1: Test New Endpoint

```python
class TestNewWorkflow:
    """Tests for new workflow."""

    def test_basic_functionality(self, validator):
        """Test basic workflow execution."""
        response = requests.post(
            f"{TestConfig.BASE_URL}/webhook/new-endpoint",
            json={"input": "test"},
            timeout=TestConfig.TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()
        validator.validate_success(data)
```

### Example 2: Test Error Cases

```python
def test_invalid_input(self):
    """Test workflow handles invalid input."""
    response = requests.post(
        TestConfig.CODE_ANALYZER_ENDPOINT,
        json={"invalid": "data"},
        timeout=TestConfig.TIMEOUT
    )

    # Should return error or 400 status
    if response.status_code == 200:
        data = response.json()
        assert data.get("success") is False
        assert "error" in data
    else:
        assert response.status_code == 400
```

### Example 3: Performance Test

```python
@pytest.mark.performance
def test_performance_sla(self, perf_tracker):
    """Test meets 5-second SLA."""
    perf_tracker.start()

    response = requests.post(
        TestConfig.CODE_ANALYZER_ENDPOINT,
        json={"code": "x=1", "language": "python"},
        timeout=TestConfig.TIMEOUT
    )

    perf_tracker.stop()

    assert response.status_code == 200
    perf_tracker.assert_within_timeout(5000)
```

## Contributing

When adding new tests:

1. Follow the existing test structure
2. Use validators and performance trackers
3. Add appropriate markers
4. Update this README if adding new categories
5. Ensure tests pass in CI/CD

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [requests documentation](https://requests.readthedocs.io/)
- [n8n documentation](https://docs.n8n.io/)
- [Claude API documentation](https://docs.anthropic.com/)
