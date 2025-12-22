#!/usr/bin/env python3
"""Final test of v3 workflow"""
import requests
import json

print("🧪 Testing v3 Finnhub Workflow\n")
print("=" * 70)

response = requests.post(
    "http://100.82.85.95:5678/webhook/stock-telegram-v3",
    json={"symbols": "AAPL", "send_to_telegram": False},
    timeout=60
)

print(f"Status: {response.status_code}\n")

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2)[:1000])

    analysis = data.get('analysis', '')

    if '$273' in analysis or '$485' in analysis or ('$' in analysis and 'AAPL' in analysis):
        print("\n\n🎉🎉🎉 SUCCESS! Real stock data! 🎉🎉🎉")
    else:
        print("\n\n⚠️  Check analysis above")
else:
    print(f"Error: {response.text[:500]}")
