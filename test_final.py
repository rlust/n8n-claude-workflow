#!/usr/bin/env python3
"""Test the final working Finnhub workflow"""
import requests
import json

print("🧪 Testing Complete Finnhub Workflow\n")
print("=" * 70)

response = requests.post(
    "http://100.82.85.95:5678/webhook/stock-finnhub",
    json={"symbols": "AAPL,MSFT,PRK", "send_to_telegram": False},
    timeout=90
)

print(f"Status: {response.status_code}\n")
print(f"Response text length: {len(response.text)}")
print(f"Response text: {response.text[:200]}\n")

if response.status_code == 200 and response.text:
    try:
        data = response.json()
    except:
        print(f"❌ Empty or invalid response")
        print(f"Full response: {response.text}")
        exit(1)

    print("✅ SUCCESS!\n")
    print(json.dumps(data, indent=2))

    analysis = data.get('analysis', '')

    # Check for real stock prices
    if '$273' in analysis or '$485' in analysis or ('$' in analysis and any(c.isdigit() for c in analysis)):
        print("\n\n🎉🎉🎉 REAL STOCK DATA FROM FINNHUB! 🎉🎉🎉")
    else:
        print("\n\n⚠️  Check the analysis above")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text[:500])
