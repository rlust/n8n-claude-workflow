# Smart Calculator Agent

A full-featured interactive calculator powered by Claude Agent SDK with command-line interface, calculation history, and natural language processing.

## Features

✨ **Interactive Command Loop** - Runs continuously until you exit
🎨 **Colorful Terminal UI** - ANSI colors for beautiful output
📜 **Calculation History** - Track all your calculations with timestamps
💬 **Natural Language** - Ask math questions in plain English
🔧 **Built-in Commands** - Help, history, clear, and exit commands
⚡ **Streaming Responses** - Real-time answers from Claude
🛡️ **Error Handling** - Graceful error messages and validation

## Installation

### 1. Install Claude Agent SDK

```bash
pip3 install claude-agent-sdk
```

### 2. Set up API Key

Get your API key from [console.anthropic.com](https://console.anthropic.com/)

```bash
# Linux/macOS
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

**For permanent setup**, add to your shell profile:

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Make Executable (Optional)

```bash
chmod +x smart_calc.py
```

## Usage

### Start the Calculator

```bash
python3 smart_calc.py
# or if made executable:
./smart_calc.py
```

### Example Session

```
╔═══════════════════════════════════════════╗
║     Smart Calculator Agent (Claude)      ║
╚═══════════════════════════════════════════╝

Type your math problem or use commands:
  /help    - Show available commands
  /history - View calculation history
  /clear   - Clear history
  /exit    - Exit the calculator

Calculate > 98*56-2
Thinking...

Answer:
Let me calculate that for you:
98 × 56 = 5,488
5,488 - 2 = 5,486

Calculate > What is 15% of 200?
Thinking...

Answer:
15% of 200 is 30.

Calculate > /history

Calculation History:
────────────────────────────────────────────────────────────
[1] 14:23:15
  Q: 98*56-2
  A: 5,486

[2] 14:23:42
  Q: What is 15% of 200?
  A: 30
────────────────────────────────────────────────────────────

Calculate > /exit
Thanks for using Smart Calculator! Goodbye!
```

## Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands and examples |
| `/history` | Display all calculations with timestamps |
| `/clear` | Clear calculation history |
| `/exit` or `/quit` | Exit the calculator |
| `Ctrl+C` | Quick exit |

## Calculation Examples

### Simple Arithmetic
```
Calculate > 15 + 27 * 3
Answer: 96
```

### Exponents
```
Calculate > 2^8
Answer: 256

Calculate > 5**3
Answer: 125
```

### Fractions
```
Calculate > 1/2 + 3/4
Answer: 1.25 or 5/4
```

### Percentages
```
Calculate > What is 15% of 200?
Answer: 30
```

### Word Problems
```
Calculate > If I have 3 apples and buy 7 more, how many do I have?
Answer: 10 apples
```

### Complex Calculations
```
Calculate > (10 + 5) * 3 - 8/2
Answer: 41
```

## Requirements

- **Python:** 3.8 or higher
- **Dependencies:**
  - `claude-agent-sdk` (0.1.17+)
  - `asyncio` (built-in)
  - `datetime` (built-in)
  - `typing` (built-in)

## How It Works

1. **User Input:** You enter a math problem or command
2. **Processing:** The input is sent to Claude via the Agent SDK
3. **AI Reasoning:** Claude solves the problem step-by-step
4. **Response:** The answer is streamed back and displayed
5. **History:** Calculation is saved with timestamp

## Architecture

```python
SmartCalculator
├── __init__()           # Initialize with system prompt and colors
├── print_banner()       # Display welcome screen
├── print_help()         # Show commands and examples
├── print_history()      # Display calculation history
├── clear_history()      # Clear saved calculations
├── calculate()          # Send query to Claude Agent SDK
├── handle_command()     # Process /help, /exit, etc.
└── run()                # Main interactive loop
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'claude_agent_sdk'"
```bash
pip3 install claude-agent-sdk
```

### "API key not found" or Authentication Error
```bash
# Check if API key is set
echo $ANTHROPIC_API_KEY

# Set it if missing
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Colors Not Displaying Correctly
- **Windows:** Use Windows Terminal or enable ANSI support
- **macOS/Linux:** Should work in any modern terminal

### Script Won't Start
```bash
# Check Python version (need 3.8+)
python3 --version

# Make executable
chmod +x smart_calc.py
```

## Advanced Usage

### Scripted Input

```bash
# Run with predefined calculations
printf "98*56-2\nWhat is 15%% of 200?\n/exit\n" | python3 smart_calc.py
```

### Custom System Prompt

Edit lines 18-24 in `smart_calc.py` to customize Claude's behavior:

```python
self.system_prompt = """
Your custom instructions here...
"""
```

### Disable Colors

Comment out the color initialization (lines 26-32) for plain text output.

## Contributing

Found a bug or want to add a feature? Feel free to modify and extend!

Potential enhancements:
- Save/load calculation history to file
- Export history to CSV/JSON
- Add graphing capabilities
- Support for variables and equations
- Unit conversions
- Scientific notation

## License

Free to use and modify.

## Credits

Built with:
- [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Anthropic Claude AI](https://www.anthropic.com/)

---

**Happy Calculating!** 🧮✨
