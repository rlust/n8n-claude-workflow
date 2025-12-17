#!/usr/bin/env python3
"""
Smart Calculator Agent
A full-featured interactive calculator powered by Claude Agent SDK
"""
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio
from datetime import datetime
from typing import List, Tuple
import sys


class SmartCalculator:
    """Interactive smart calculator agent with history and commands"""

    def __init__(self):
        self.history: List[Tuple[str, str, datetime]] = []
        self.system_prompt = """
You are a smart calculator assistant.
Solve math problems step by step when needed.
Handle arithmetic (+, -, *, /), exponents, parentheses, fractions, percentages, and word problems.
Be concise but show your work for complex calculations.
Always provide the final answer clearly.
"""
        # ANSI color codes
        self.BLUE = "\033[94m"
        self.GREEN = "\033[92m"
        self.YELLOW = "\033[93m"
        self.RED = "\033[91m"
        self.CYAN = "\033[96m"
        self.RESET = "\033[0m"
        self.BOLD = "\033[1m"

    def print_banner(self):
        """Display welcome banner"""
        print(f"\n{self.CYAN}{self.BOLD}╔═══════════════════════════════════════════╗{self.RESET}")
        print(f"{self.CYAN}{self.BOLD}║     Smart Calculator Agent (Claude)      ║{self.RESET}")
        print(f"{self.CYAN}{self.BOLD}╚═══════════════════════════════════════════╝{self.RESET}\n")
        print(f"{self.YELLOW}Type your math problem or use commands:{self.RESET}")
        print(f"  {self.GREEN}/help{self.RESET}    - Show available commands")
        print(f"  {self.GREEN}/history{self.RESET} - View calculation history")
        print(f"  {self.GREEN}/clear{self.RESET}   - Clear history")
        print(f"  {self.GREEN}/exit{self.RESET}    - Exit the calculator\n")

    def print_help(self):
        """Display help information"""
        print(f"\n{self.BLUE}{self.BOLD}Available Commands:{self.RESET}")
        print(f"  {self.GREEN}/help{self.RESET}     - Show this help message")
        print(f"  {self.GREEN}/history{self.RESET}  - Show all previous calculations")
        print(f"  {self.GREEN}/clear{self.RESET}    - Clear calculation history")
        print(f"  {self.GREEN}/exit{self.RESET}     - Exit the calculator (or Ctrl+C)")
        print(f"\n{self.BLUE}{self.BOLD}Example Calculations:{self.RESET}")
        print(f"  • Simple: {self.CYAN}15 + 27 * 3{self.RESET}")
        print(f"  • Exponents: {self.CYAN}2^8 or 5**3{self.RESET}")
        print(f"  • Fractions: {self.CYAN}1/2 + 3/4{self.RESET}")
        print(f"  • Percentages: {self.CYAN}What is 15% of 200?{self.RESET}")
        print(f"  • Word problems: {self.CYAN}If I have 3 apples and buy 7 more, how many do I have?{self.RESET}\n")

    def print_history(self):
        """Display calculation history"""
        if not self.history:
            print(f"\n{self.YELLOW}No calculation history yet.{self.RESET}\n")
            return

        print(f"\n{self.BLUE}{self.BOLD}Calculation History:{self.RESET}")
        print(f"{self.BLUE}{'─' * 60}{self.RESET}")
        for idx, (question, answer, timestamp) in enumerate(self.history, 1):
            time_str = timestamp.strftime("%H:%M:%S")
            print(f"\n{self.CYAN}[{idx}] {time_str}{self.RESET}")
            print(f"  Q: {question}")
            print(f"  A: {self.GREEN}{answer}{self.RESET}")
        print(f"{self.BLUE}{'─' * 60}{self.RESET}\n")

    def clear_history(self):
        """Clear calculation history"""
        self.history.clear()
        print(f"\n{self.GREEN}✓ History cleared.{self.RESET}\n")

    async def calculate(self, user_query: str) -> str:
        """Send query to Claude and get response"""
        options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            allowed_tools=[]  # Pure reasoning, no tool use
        )

        response_parts = []
        try:
            async for message in query(prompt=user_query, options=options):
                if hasattr(message, 'text') and message.text:
                    response_parts.append(message.text)
        except Exception as e:
            return f"Error: {str(e)}"

        return "".join(response_parts)

    def handle_command(self, command: str) -> bool:
        """Handle special commands. Returns True if should continue, False if should exit"""
        command = command.lower().strip()

        if command in ["/exit", "/quit"]:
            print(f"\n{self.CYAN}Thanks for using Smart Calculator! Goodbye!{self.RESET}\n")
            return False
        elif command == "/help":
            self.print_help()
        elif command == "/history":
            self.print_history()
        elif command == "/clear":
            self.clear_history()
        else:
            print(f"\n{self.RED}Unknown command: {command}{self.RESET}")
            print(f"Type {self.GREEN}/help{self.RESET} for available commands.\n")

        return True

    async def run(self):
        """Main interactive loop"""
        self.print_banner()

        while True:
            try:
                # Get user input
                user_input = input(f"{self.BOLD}Calculate >{self.RESET} ").strip()

                # Skip empty input
                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    if not self.handle_command(user_input):
                        break
                    continue

                # Process calculation
                print(f"\n{self.YELLOW}Thinking...{self.RESET}")
                answer = await self.calculate(user_input)

                # Display result
                print(f"\n{self.GREEN}{self.BOLD}Answer:{self.RESET}")
                print(f"{answer}\n")

                # Save to history
                self.history.append((user_input, answer, datetime.now()))

            except KeyboardInterrupt:
                print(f"\n\n{self.CYAN}Thanks for using Smart Calculator! Goodbye!{self.RESET}\n")
                break
            except EOFError:
                print(f"\n\n{self.CYAN}Thanks for using Smart Calculator! Goodbye!{self.RESET}\n")
                break
            except Exception as e:
                print(f"\n{self.RED}Error: {str(e)}{self.RESET}\n")


async def main():
    """Entry point"""
    calculator = SmartCalculator()
    await calculator.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
