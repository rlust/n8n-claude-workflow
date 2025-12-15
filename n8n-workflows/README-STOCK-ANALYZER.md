# Claude Stock Market Analyzer - Improved Version

This workflow uses Claude AI to provide intelligent stock market analysis with real-time data from Yahoo Finance.

## What's New in v2

✨ **Improvements:**
- **Clean Data Formatting** - Removes null values and formats data properly
- **Better Claude Prompts** - More detailed instructions for better analysis
- **Enhanced Response** - Includes company names, price changes, and detailed metrics
- **Robust Error Handling** - Handles missing data gracefully
- **Professional Output** - Structured markdown analysis

## Features

- 📊 **Real-time Stock Data** - Fetches current market data from Yahoo Finance
- 🤖 **AI-Powered Analysis** - Claude analyzes trends, volumes, and patterns
- 🎯 **Two Analysis Modes**:
  - **Overview** - Quick market summary and outlook
  - **Detailed** - Comprehensive analysis with trading recommendations
- 📈 **Multiple Stocks** - Analyze up to 2 stocks simultaneously
- ⚡ **Fast Response** - Results in ~10-15 seconds

## Installation

### 1. Import into n8n

1. Download `claude-stock-market-analyzer-v2.json`
2. In n8n: **Workflows** → **Import from File**
3. Select the downloaded file
4. Click **Import**

### 2. Configure API Credentials

1. Click on **"Call Claude API"** node
2. Select your Anthropic API credential (x-api-key)
3. Click **Save**

### 3. Activate Workflow

1. Click the toggle at top-right to **Activate**
2. The webhook will be available at: `/webhook/stock-analysis`

## Usage

### Major Stock Market Indexes (Default)

```bash
# S&P 500 and Dow Jones (default if no symbols provided)
curl -X POST http://your-n8n-url:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Analyze Multiple Indexes

```bash
# Compare S&P 500, NASDAQ, and VIX
curl -X POST http://your-n8n-url:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "^GSPC,^IXIC",
    "analysis_type": "overview"
  }'
```

### Individual Stocks Analysis

```bash
curl -X POST http://your-n8n-url:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "AAPL,MSFT",
    "analysis_type": "overview"
  }'
```

### Detailed Market Analysis

```bash
# Detailed analysis with trading recommendations
curl -X POST http://your-n8n-url:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "^GSPC,SPY",
    "analysis_type": "detailed"
  }'
```

### Mix Indexes and Stocks

```bash
# Compare S&P 500 index with tech stocks
curl -X POST http://your-n8n-url:5678/webhook/stock-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": "^GSPC,AAPL",
    "analysis_type": "detailed"
  }'
```

## Response Format

```json
{
  "success": true,
  "symbols": "AAPL,MSFT",
  "analysis": "# Stock Market Analysis\n\n## AAPL (Apple Inc.)\n...",
  "metadata": {
    "model": "claude-sonnet-4-5-20250929",
    "tokens_used": 1234,
    "analyzed_at": "2025-12-15T19:30:00.000Z"
  }
}
```

## What Claude Analyzes

### Overview Mode
- Current price vs previous close
- Price trend direction (bullish/bearish/neutral)
- Notable price movements
- Volume insights
- Quick outlook

### Detailed Mode
- **Price Trends** - Uptrends, downtrends, consolidation patterns
- **Volume Analysis** - Trading activity and liquidity assessment
- **Support/Resistance** - Key price levels to watch
- **Market Sentiment** - Overall market mood
- **Trading Recommendations** - Actionable bullish/bearish/neutral signals
- **Risk Assessment** - Opportunities and potential risks
- **Comparative Analysis** - How stocks compare to each other

## Data Provided to Claude

For each stock, Claude receives:

```json
{
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "currency": "USD",
  "exchange": "NASDAQ",
  "current_price": 195.89,
  "previous_close": 194.50,
  "price_change": 1.39,
  "price_change_percent": "0.71%",
  "day_high": 196.50,
  "day_low": 194.20,
  "prices": [
    {
      "date": "2025-12-11",
      "open": 193.50,
      "high": 195.00,
      "low": 192.80,
      "close": 194.50,
      "volume": 45000000
    }
    // ... more days
  ],
  "data_points": 5,
  "period": "Last 5 trading days"
}
```

## Supported Symbols

### Major Stock Market Indexes
- **^GSPC** - S&P 500 Index
- **^DJI** - Dow Jones Industrial Average
- **^IXIC** - NASDAQ Composite
- **^RUT** - Russell 2000
- **^VIX** - Volatility Index (Fear Index)
- **^FTSE** - FTSE 100 (UK)
- **^N225** - Nikkei 225 (Japan)

### Popular ETFs (Index Trackers)
- **SPY** - SPDR S&P 500 ETF
- **QQQ** - Invesco QQQ (Nasdaq-100)
- **DIA** - SPDR Dow Jones Industrial Average
- **IWM** - iShares Russell 2000
- **VTI** - Vanguard Total Stock Market

### Individual Stocks
- **US Markets**: AAPL, MSFT, GOOGL, TSLA, NVDA, AMZN, META, etc.
- **International**: Many global stocks (format may vary)

## Cost Estimate

Using Claude Sonnet 4.5:
- **Overview analysis**: ~500-800 tokens ($0.002-0.003)
- **Detailed analysis**: ~1,500-2,500 tokens ($0.005-0.008)

## Troubleshooting

### "No data available" error
- Check if markets are open or use valid stock symbols
- Yahoo Finance may have rate limits
- Try again in a few seconds

### Empty response
- Ensure workflow is **Activated**
- Check **Executions** tab for errors
- Verify API credentials are configured

### Claude says "data is null"
- This shouldn't happen in v2!
- Check the "Clean Stock Data" node output
- Ensure Yahoo Finance is responding

## Technical Details

### Workflow Architecture

```
Webhook → Extract Parameters → Fetch Stock Data (parallel)
         ↓
    Merge → Clean Data → Format → Claude → Response
```

### Key Improvements in v2

1. **Clean Stock Data Node** (JavaScript)
   - Extracts data from Yahoo Finance's nested structure
   - Filters out null values from non-trading days
   - Calculates price changes and percentages
   - Formats dates properly

2. **Better Prompts**
   - More specific instructions for Claude
   - Structured analysis requirements
   - Clear formatting guidelines

3. **Enhanced Metadata**
   - Company names, not just symbols
   - Exchange information
   - Intraday high/low prices

## Integration Ideas

### Slack Bot
```
Schedule Node (daily at market close)
    ↓
Stock Analyzer
    ↓
Format Message → Slack
```

### Email Digest
```
Cron (Mon-Fri 9am)
    ↓
Stock Analyzer
    ↓
Email Node → Send digest
```

### Discord Alerts
```
Webhook Trigger
    ↓
Stock Analyzer
    ↓
Discord Webhook → Post analysis
```

## Changelog

### v2.0 (2025-12-15)
- ✨ Added "Clean Stock Data" node with proper data extraction
- ✨ Improved Claude prompts for better analysis quality
- ✨ Enhanced response with company names and metadata
- 🐛 Fixed null data issues from Yahoo Finance
- 📝 Added comprehensive documentation

### v1.0 (2025-12-15)
- 🎉 Initial release
- Basic stock data fetching
- Claude integration

## Support

For issues or questions:
- Check n8n Executions tab for errors
- Review the workflow in test mode
- Verify API credentials are valid

## License

MIT License - Free to use and modify

## Credits

- Built with n8n workflow automation
- Powered by Claude AI (Anthropic)
- Market data from Yahoo Finance

---

**Disclaimer**: This tool provides information only and should not be considered financial advice. Always consult with a qualified financial advisor before making investment decisions.
