#!/usr/bin/env python3
"""Test the 5-stock workflow"""
import requests
import json

webhook_url = "http://100.82.85.95:5678/webhook/stock-telegram-v3"
payload = {
    "symbols": "AAPL,MSFT,PRK,QQQ,F",
    "send_to_telegram": False
}

print("🧪 Testing workflow with 5 stocks...")
print(f"📊 Stocks: {payload['symbols']}\n")

try:
    response = requests.post(webhook_url, json=payload, timeout=90)

    if response.status_code == 200:
        data = response.json()
        print("✅ Workflow executed successfully!")
        print(f"\n📈 Results:")
        print(f"   Stocks analyzed: {data.get('symbols', 'N/A')}")
        print(f"   Tokens used: {data.get('tokens_used', 'N/A')}")
        print(f"   Telegram sent: {data.get('telegram_sent', False)}")

        analysis = data.get('analysis', '')
        print(f"\n📝 Analysis Preview (first 600 chars):")
        print("=" * 60)
        print(analysis[:600])
        print("...")
        print("=" * 60)

    else:
        print(f"❌ Request failed with status: {response.status_code}")
        print(f"Response: {response.text[:500]}")

except Exception as e:
    print(f"❌ Error: {e}")
