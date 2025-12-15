.PHONY: help install test test-fast test-slow test-coverage test-html clean lint

help:
	@echo "Available commands:"
	@echo "  make install        - Install test dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make test-fast     - Run fast tests only (skip slow agent tests)"
	@echo "  make test-slow     - Run only slow tests"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make test-html     - Run tests and generate HTML report"
	@echo "  make lint          - Run code linting"
	@echo "  make clean         - Clean test artifacts"

install:
	pip install -r tests/requirements.txt

test:
	pytest tests/ -v

test-fast:
	pytest tests/ -m "not slow" -v

test-slow:
	pytest tests/ -m "slow" -v

test-coverage:
	pytest tests/ -v --cov=tests --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

test-html:
	pytest tests/ -v --html=test-results/report.html --self-contained-html
	@echo "Test report generated in test-results/report.html"

test-parallel:
	pytest tests/ -v -n auto

test-debug:
	pytest tests/ -vv --tb=long --showlocals -s

lint:
	flake8 tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf test-results/
	rm -rf .coverage
	rm -rf .benchmarks/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
