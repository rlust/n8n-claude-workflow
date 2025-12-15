"""
Pytest configuration and shared fixtures for n8n workflow tests.
"""

import pytest
import os


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "performance: mark test as performance test")
    config.addinivalue_line("markers", "agent: mark test as using Claude Agent SDK")
    config.addinivalue_line("markers", "api: mark test as using Claude API")


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their class."""
    for item in items:
        # Auto-mark based on test class name
        if "Agent" in item.nodeid:
            item.add_marker(pytest.mark.agent)
            item.add_marker(pytest.mark.slow)

        if "Performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)

        if "Test" in item.nodeid:
            item.add_marker(pytest.mark.integration)

        # Mark all as API tests by default
        item.add_marker(pytest.mark.api)


@pytest.fixture(scope="session")
def base_url():
    """Provide the base URL for n8n workflows."""
    return os.getenv("N8N_BASE_URL", "http://100.82.85.95:5678")


@pytest.fixture(scope="session")
def default_timeout():
    """Provide default timeout for requests."""
    return int(os.getenv("TEST_TIMEOUT", "30"))


@pytest.fixture
def sample_code():
    """Provide sample code snippets for testing."""
    return {
        "javascript": "function add(a, b) { return a + b; }",
        "python": "def add(a, b):\n    return a + b",
        "java": "public int add(int a, int b) { return a + b; }",
    }


@pytest.fixture
def sample_document():
    """Provide sample document for summarization testing."""
    return """
    Artificial intelligence (AI) is intelligence demonstrated by machines,
    in contrast to the natural intelligence displayed by humans and animals.
    Leading AI textbooks define the field as the study of "intelligent agents":
    any device that perceives its environment and takes actions that maximize
    its chance of successfully achieving its goals. Machine learning is a
    subset of AI that focuses on the development of algorithms that can learn
    from and make predictions or decisions based on data.
    """
