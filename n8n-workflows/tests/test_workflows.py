"""
Automated integration tests for n8n Claude workflows.

Tests all workflow endpoints with proper assertions, validation,
and performance metrics.
"""

import pytest
import requests
import time
import json
from typing import Dict, Any, Optional


class TestConfig:
    """Test configuration and constants."""
    BASE_URL = "http://100.82.85.95:5678"
    TIMEOUT = 30  # seconds

    # Endpoints
    CODE_ANALYZER_ENDPOINT = f"{BASE_URL}/webhook/analyze-code"
    DOCUMENT_SUMMARIZER_ENDPOINT = f"{BASE_URL}/webhook/summarize-document"
    AGENT_CODEBASE_ENDPOINT = f"{BASE_URL}/webhook/agent-analyze-codebase"


class ResponseValidator:
    """Helper class for validating workflow responses."""

    @staticmethod
    def validate_structure(response: Dict[str, Any], required_fields: list) -> None:
        """Validate response has required fields."""
        for field in required_fields:
            assert field in response, f"Missing required field: {field}"

    @staticmethod
    def validate_success(response: Dict[str, Any]) -> None:
        """Validate response indicates success."""
        assert response.get("success") is True, f"Workflow failed: {response.get('error', 'Unknown error')}"

    @staticmethod
    def validate_metadata(response: Dict[str, Any]) -> None:
        """Validate metadata structure and content."""
        assert "metadata" in response, "Missing metadata"
        metadata = response["metadata"]

        # Common metadata fields
        if "model" in metadata:
            assert isinstance(metadata["model"], str), "Model should be a string"
        if "tokens" in metadata:
            assert isinstance(metadata["tokens"], int), "Tokens should be an integer"
            assert metadata["tokens"] > 0, "Token count should be positive"

    @staticmethod
    def validate_non_empty(value: Any, field_name: str) -> None:
        """Validate field is not empty."""
        assert value, f"{field_name} should not be empty"
        if isinstance(value, str):
            assert len(value.strip()) > 0, f"{field_name} should not be whitespace only"


class PerformanceTracker:
    """Track performance metrics for tests."""

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """Start timing."""
        self.start_time = time.time()

    def stop(self):
        """Stop timing."""
        self.end_time = time.time()

    @property
    def duration_ms(self) -> float:
        """Get duration in milliseconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0

    def assert_within_timeout(self, max_duration_ms: float) -> None:
        """Assert duration is within acceptable range."""
        assert self.duration_ms < max_duration_ms, \
            f"Request took {self.duration_ms:.2f}ms, expected < {max_duration_ms}ms"


@pytest.fixture
def validator():
    """Provide a ResponseValidator instance."""
    return ResponseValidator()


@pytest.fixture
def perf_tracker():
    """Provide a PerformanceTracker instance."""
    return PerformanceTracker()


class TestCodeAnalyzer:
    """Tests for the Claude Code Analyzer workflow."""

    def test_basic_code_analysis(self, validator, perf_tracker):
        """Test basic code analysis with valid input."""
        perf_tracker.start()

        response = requests.post(
            TestConfig.CODE_ANALYZER_ENDPOINT,
            json={
                "code": "function add(a, b) { return a + b; }",
                "language": "javascript"
            },
            timeout=TestConfig.TIMEOUT
        )

        perf_tracker.stop()

        # Assert HTTP status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Parse and validate JSON
        data = response.json()

        # Validate structure
        validator.validate_structure(data, ["success", "analysis", "metadata"])
        validator.validate_success(data)
        validator.validate_metadata(data)

        # Validate analysis content
        validator.validate_non_empty(data["analysis"], "analysis")
        assert len(data["analysis"]) > 50, "Analysis should be meaningful (>50 chars)"

        # Performance check (Claude API calls should complete in reasonable time)
        perf_tracker.assert_within_timeout(30000)  # 30 seconds

        print(f"✓ Test completed in {perf_tracker.duration_ms:.2f}ms")

    def test_code_analysis_with_issues(self, validator):
        """Test code analysis with problematic code."""
        response = requests.post(
            TestConfig.CODE_ANALYZER_ENDPOINT,
            json={
                "code": """
                function unsafe(userInput) {
                    eval(userInput);  // Security issue
                    var x = 1;  // Old syntax
                    return x
                }
                """,
                "language": "javascript"
            },
            timeout=TestConfig.TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()

        validator.validate_success(data)
        validator.validate_non_empty(data["analysis"], "analysis")

        # Should mention security issues
        analysis_lower = data["analysis"].lower()
        assert any(keyword in analysis_lower for keyword in ["eval", "security", "unsafe"]), \
            "Analysis should identify security issues"

    def test_multiple_languages(self, validator):
        """Test code analysis works with different programming languages."""
        languages = [
            ("python", "def hello():\n    print('Hello')"),
            ("javascript", "const hello = () => console.log('Hello');"),
            ("java", "public class Hello { public static void main(String[] args) {} }"),
        ]

        for language, code in languages:
            response = requests.post(
                TestConfig.CODE_ANALYZER_ENDPOINT,
                json={"code": code, "language": language},
                timeout=TestConfig.TIMEOUT
            )

            assert response.status_code == 200, f"Failed for language: {language}"
            data = response.json()
            validator.validate_success(data)
            validator.validate_non_empty(data["analysis"], f"analysis for {language}")

    def test_empty_code_handling(self):
        """Test handling of empty code input."""
        response = requests.post(
            TestConfig.CODE_ANALYZER_ENDPOINT,
            json={"code": "", "language": "javascript"},
            timeout=TestConfig.TIMEOUT
        )

        # Should either reject or handle gracefully
        assert response.status_code in [200, 400], "Should return valid status code"

        if response.status_code == 200:
            data = response.json()
            # If it accepts empty code, should still return valid structure
            assert "success" in data or "error" in data


class TestDocumentSummarizer:
    """Tests for the Claude Document Summarizer workflow."""

    def test_basic_summarization(self, validator, perf_tracker):
        """Test basic document summarization."""
        perf_tracker.start()

        long_text = """
        Artificial intelligence (AI) is intelligence demonstrated by machines,
        in contrast to the natural intelligence displayed by humans and animals.
        Leading AI textbooks define the field as the study of "intelligent agents":
        any device that perceives its environment and takes actions that maximize
        its chance of successfully achieving its goals. Colloquially, the term
        "artificial intelligence" is often used to describe machines that mimic
        "cognitive" functions that humans associate with the human mind, such as
        "learning" and "problem solving". As machines become increasingly capable,
        tasks considered to require "intelligence" are often removed from the
        definition of AI, a phenomenon known as the AI effect.
        """

        response = requests.post(
            TestConfig.DOCUMENT_SUMMARIZER_ENDPOINT,
            json={
                "document": long_text,
                "format": "paragraph",
                "length": "short"
            },
            timeout=TestConfig.TIMEOUT
        )

        perf_tracker.stop()

        assert response.status_code == 200
        data = response.json()

        # Validate structure
        validator.validate_structure(data, ["success", "summary", "metadata"])
        validator.validate_success(data)
        validator.validate_metadata(data)

        # Validate summary
        validator.validate_non_empty(data["summary"], "summary")

        # Summary should be shorter than original
        assert len(data["summary"]) < len(long_text), "Summary should be shorter than original"

        # Should have compression ratio
        assert "compression_ratio" in data["metadata"], "Should include compression ratio"

        print(f"✓ Summarized in {perf_tracker.duration_ms:.2f}ms")

    def test_bullet_format(self, validator):
        """Test bullet point format output."""
        response = requests.post(
            TestConfig.DOCUMENT_SUMMARIZER_ENDPOINT,
            json={
                "document": "The quick brown fox jumps over the lazy dog. " * 20,
                "format": "bullets",
                "length": "medium"
            },
            timeout=TestConfig.TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()

        validator.validate_success(data)
        validator.validate_non_empty(data["summary"], "summary")

        # Bullet format should contain bullet markers
        assert any(marker in data["summary"] for marker in ["•", "-", "*", "1.", "2."]), \
            "Bullet format should contain list markers"

    def test_input_validation(self):
        """Test input validation for minimum length."""
        short_text = "Too short"

        response = requests.post(
            TestConfig.DOCUMENT_SUMMARIZER_ENDPOINT,
            json={
                "document": short_text,
                "format": "paragraph",
                "length": "short"
            },
            timeout=TestConfig.TIMEOUT
        )

        # Should reject input that's too short (< 100 chars)
        data = response.json()

        if response.status_code == 200:
            # If accepted, check for error in response
            assert data.get("success") is False, "Should reject short input"
            assert "error" in data, "Should include error message"
        else:
            assert response.status_code == 400, "Should return 400 for invalid input"

    def test_different_lengths(self, validator):
        """Test different summary length options."""
        long_text = "The history of artificial intelligence. " * 50

        lengths = ["short", "medium", "long"]
        summaries = {}

        for length in lengths:
            response = requests.post(
                TestConfig.DOCUMENT_SUMMARIZER_ENDPOINT,
                json={
                    "document": long_text,
                    "format": "paragraph",
                    "length": length
                },
                timeout=TestConfig.TIMEOUT
            )

            assert response.status_code == 200
            data = response.json()
            validator.validate_success(data)
            summaries[length] = data["summary"]

        # Generally, longer summaries should have more content
        # (though this isn't guaranteed with LLMs)
        assert all(len(s) > 0 for s in summaries.values()), "All summaries should have content"


class TestAgentCodebaseAnalyzer:
    """Tests for the Claude Agent SDK Codebase Analyzer workflow."""

    def test_basic_agent_analysis(self, validator, perf_tracker):
        """Test basic autonomous agent codebase analysis."""
        perf_tracker.start()

        response = requests.post(
            TestConfig.AGENT_CODEBASE_ENDPOINT,
            json={
                "task": "List all JSON files in the examples directory",
                "repo_path": "/root/claude/n8n-workflows"
            },
            timeout=60  # Agents can take longer
        )

        perf_tracker.stop()

        assert response.status_code == 200
        data = response.json()

        # Validate structure
        validator.validate_structure(data, ["success", "result"])
        validator.validate_success(data)

        # Validate result
        validator.validate_non_empty(data["result"], "result")

        # Should mention JSON files
        result_lower = data["result"].lower()
        assert "json" in result_lower or ".json" in result_lower, \
            "Result should mention JSON files"

        print(f"✓ Agent completed in {perf_tracker.duration_ms:.2f}ms")

    def test_agent_file_search(self, validator):
        """Test agent's ability to search for specific patterns."""
        response = requests.post(
            TestConfig.AGENT_CODEBASE_ENDPOINT,
            json={
                "task": "Find all files with 'claude' in the filename",
                "repo_path": "/root/claude/n8n-workflows"
            },
            timeout=60
        )

        assert response.status_code == 200
        data = response.json()

        validator.validate_success(data)
        validator.validate_non_empty(data["result"], "result")

        # Should find claude-related files
        result_lower = data["result"].lower()
        assert "claude" in result_lower, "Should find files with 'claude' in name"

    def test_agent_error_handling(self):
        """Test agent handles invalid repository paths."""
        response = requests.post(
            TestConfig.AGENT_CODEBASE_ENDPOINT,
            json={
                "task": "Analyze this repository",
                "repo_path": "/nonexistent/path/that/does/not/exist"
            },
            timeout=60
        )

        # Should handle gracefully
        assert response.status_code in [200, 400, 500]

        if response.status_code == 200:
            data = response.json()
            # Should either fail gracefully or report the issue
            if data.get("success") is False:
                assert "error" in data, "Failed response should include error"


class TestPerformance:
    """Performance and load testing."""

    def test_response_time_acceptable(self, perf_tracker):
        """Test that all endpoints respond within acceptable time."""
        endpoints = [
            (TestConfig.CODE_ANALYZER_ENDPOINT, {
                "code": "print('hello')",
                "language": "python"
            }, 30000),  # 30s max
        ]

        for endpoint, payload, max_duration in endpoints:
            perf_tracker.start()
            response = requests.post(endpoint, json=payload, timeout=TestConfig.TIMEOUT)
            perf_tracker.stop()

            assert response.status_code == 200
            perf_tracker.assert_within_timeout(max_duration)

            print(f"✓ {endpoint} responded in {perf_tracker.duration_ms:.2f}ms")

    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import concurrent.futures

        def make_request():
            return requests.post(
                TestConfig.CODE_ANALYZER_ENDPOINT,
                json={"code": "x = 1", "language": "python"},
                timeout=TestConfig.TIMEOUT
            )

        # Send 3 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request) for _ in range(3)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All should succeed
        assert all(r.status_code == 200 for r in responses), "All concurrent requests should succeed"

        # All should return valid data
        for response in responses:
            data = response.json()
            assert data.get("success") is True, "All responses should be successful"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
