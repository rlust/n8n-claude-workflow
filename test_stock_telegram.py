#!/usr/bin/env python3
"""
Test script for Stock Analysis to Telegram workflow
Tests the n8n workflow without requiring Anthropic API or Telegram credentials
"""
import requests
import json
import sys
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class StockWorkflowTester:
    """Test the Stock to Telegram n8n workflow"""

    def __init__(self, n8n_url="http://100.82.85.95:5678"):
        self.n8n_url = n8n_url
        self.webhook_path = "/webhook/stock-to-telegram"
        self.webhook_url = f"{n8n_url}{self.webhook_path}"

    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{text}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")

    def print_success(self, text):
        """Print success message"""
        print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

    def print_error(self, text):
        """Print error message"""
        print(f"{Colors.RED}✗ {text}{Colors.RESET}")

    def print_info(self, text):
        """Print info message"""
        print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

    def test_workflow_exists(self):
        """Test if the workflow webhook is accessible"""
        self.print_header("Test 1: Check if workflow is active")

        try:
            # Try a simple GET request to see if endpoint exists
            response = requests.get(self.webhook_url, timeout=5)

            # n8n webhooks typically return 404 or error for GET requests
            # We just want to check if the endpoint is reachable
            if response.status_code in [404, 405, 500]:
                self.print_success(f"Webhook endpoint is reachable at {self.webhook_url}")
                return True
            else:
                self.print_info(f"Webhook responded with status code: {response.status_code}")
                return True

        except requests.exceptions.ConnectionError:
            self.print_error(f"Cannot connect to n8n at {self.n8n_url}")
            self.print_info("Make sure n8n is running and accessible")
            return False
        except requests.exceptions.Timeout:
            self.print_error("Connection timeout")
            return False
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False

    def test_workflow_execution(self, symbols="AAPL,MSFT", analysis_type="overview",
                                send_to_telegram=False, chat_id=None):
        """Test workflow execution with specific parameters"""

        test_name = f"Test: {symbols} ({analysis_type})"
        self.print_header(test_name)

        payload = {
            "symbols": symbols,
            "analysis_type": analysis_type,
            "chat_id": chat_id,
            "send_to_telegram": send_to_telegram
        }

        self.print_info(f"Request payload:")
        print(f"{Colors.CYAN}{json.dumps(payload, indent=2)}{Colors.RESET}\n")

        try:
            self.print_info("Sending request to webhook...")
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=60  # Stock analysis can take time
            )

            print(f"\n{Colors.BOLD}Response Status:{Colors.RESET} {response.status_code}")

            if response.status_code == 200:
                self.print_success("Workflow executed successfully!")

                try:
                    result = response.json()
                    print(f"\n{Colors.BOLD}Response Data:{Colors.RESET}")
                    print(f"{Colors.CYAN}{json.dumps(result, indent=2)}{Colors.RESET}\n")

                    # Validate response structure
                    if result.get("success"):
                        self.print_success("Response indicates success")

                        if "analysis" in result:
                            self.print_success("Analysis text present")
                            print(f"\n{Colors.BOLD}Analysis Preview:{Colors.RESET}")
                            analysis = result["analysis"]
                            preview = analysis[:300] + "..." if len(analysis) > 300 else analysis
                            print(f"{Colors.YELLOW}{preview}{Colors.RESET}\n")

                        if "tokens_used" in result:
                            self.print_success(f"Tokens used: {result['tokens_used']}")

                        if result.get("telegram_message_id"):
                            self.print_success(f"Telegram message sent (ID: {result['telegram_message_id']})")
                        elif not send_to_telegram:
                            self.print_info("Telegram sending was disabled")

                        return True, result
                    else:
                        self.print_error("Response indicates failure")
                        return False, result

                except json.JSONDecodeError:
                    self.print_error("Response is not valid JSON")
                    print(f"{Colors.YELLOW}Response text:{Colors.RESET}\n{response.text}\n")
                    return False, None

            elif response.status_code == 404:
                self.print_error("Webhook not found (404)")
                self.print_info("Make sure the workflow is imported and activated in n8n")
                return False, None

            elif response.status_code == 500:
                self.print_error("Internal server error (500)")
                self.print_info("Check n8n logs for errors")
                try:
                    error_data = response.json()
                    print(f"{Colors.YELLOW}Error details:{Colors.RESET}\n{json.dumps(error_data, indent=2)}\n")
                except:
                    print(f"{Colors.YELLOW}Response:{Colors.RESET}\n{response.text}\n")
                return False, None

            else:
                self.print_error(f"Unexpected status code: {response.status_code}")
                print(f"{Colors.YELLOW}Response:{Colors.RESET}\n{response.text}\n")
                return False, None

        except requests.exceptions.Timeout:
            self.print_error("Request timeout (workflow may still be running)")
            self.print_info("Check n8n executions panel to see if workflow completed")
            return False, None

        except requests.exceptions.ConnectionError:
            self.print_error(f"Cannot connect to {self.webhook_url}")
            return False, None

        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False, None

    def run_all_tests(self):
        """Run comprehensive test suite"""
        self.print_header("🧪 Stock to Telegram Workflow Test Suite")
        print(f"{Colors.BOLD}Testing workflow at:{Colors.RESET} {self.webhook_url}")
        print(f"{Colors.BOLD}Timestamp:{Colors.RESET} {datetime.now().isoformat()}\n")

        results = []

        # Test 1: Check if workflow exists
        workflow_exists = self.test_workflow_exists()
        if not workflow_exists:
            self.print_error("Cannot proceed - workflow is not accessible")
            return

        # Test 2: Basic test with default parameters (no Telegram)
        success, result = self.test_workflow_execution(
            symbols="AAPL,MSFT",
            analysis_type="overview",
            send_to_telegram=False
        )
        results.append(("Basic Test (AAPL,MSFT)", success))

        # Test 3: Market indices
        success, result = self.test_workflow_execution(
            symbols="^GSPC,^DJI",
            analysis_type="overview",
            send_to_telegram=False
        )
        results.append(("Market Indices Test", success))

        # Test 4: Detailed analysis
        success, result = self.test_workflow_execution(
            symbols="TSLA,NVDA",
            analysis_type="detailed",
            send_to_telegram=False
        )
        results.append(("Detailed Analysis Test", success))

        # Print summary
        self.print_header("📊 Test Summary")
        passed = sum(1 for _, success in results if success)
        total = len(results)

        for test_name, success in results:
            if success:
                self.print_success(f"{test_name}")
            else:
                self.print_error(f"{test_name}")

        print(f"\n{Colors.BOLD}Total:{Colors.RESET} {passed}/{total} tests passed")

        if passed == total:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed!{Colors.RESET}\n")
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Some tests failed{Colors.RESET}\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Test Stock to Telegram n8n workflow")
    parser.add_argument("--url", default="http://100.82.85.95:5678",
                       help="n8n instance URL (default: http://100.82.85.95:5678)")
    parser.add_argument("--symbols", help="Stock symbols to test (e.g., AAPL,MSFT)")
    parser.add_argument("--detailed", action="store_true", help="Use detailed analysis")
    parser.add_argument("--telegram", action="store_true", help="Enable Telegram sending")
    parser.add_argument("--chat-id", default=None, help="Telegram chat ID (optional, will use workflow default)")
    parser.add_argument("--all", action="store_true", help="Run all tests")

    args = parser.parse_args()

    tester = StockWorkflowTester(n8n_url=args.url)

    if args.all:
        tester.run_all_tests()
    elif args.symbols:
        analysis_type = "detailed" if args.detailed else "overview"
        tester.test_workflow_execution(
            symbols=args.symbols,
            analysis_type=analysis_type,
            send_to_telegram=args.telegram,
            chat_id=args.chat_id
        )
    else:
        # Default: run all tests
        tester.run_all_tests()


if __name__ == "__main__":
    main()
