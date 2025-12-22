#!/usr/bin/env python3
"""Test the Finnhub workflow"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv('WEBHOOK_URL_FINNHUB', 'http://100.82.85.95:5678/webhook/stock-telegram-v4-finnhub')

print("=" * 70)
print("🧪 Testing Finnhub Workflow")
print("=" * 70)

print(f"\n🌐 Webhook URL: {WEBHOOK_URL}")

# Test 1: Simple test without Telegram
print("\n" + "=" * 70)
print("📊 TEST 1: Fetch stock data (no Telegram)")
print("=" * 70)

payload1 = {
    "symbols": "AAPL,MSFT",
    "send_to_telegram": False
}

print(f"\n📤 Request:")
print(json.dumps(payload1, indent=2))

try:
    response1 = requests.post(WEBHOOK_URL, json=payload1, timeout=120)

    print(f"\n📥 Response:")
    print(f"   Status: {response1.status_code}")

    if response1.status_code == 200:
        data = response1.json()
        print(f"\n✅ Success!")
        print(json.dumps(data, indent=2))

        # Check for stock data
        if 'analysis' in data and data['analysis']:
            print(f"\n📊 Analysis generated!")
            print(f"   Stocks: {data.get('symbols')}")
            print(f"   Tokens: {data.get('tokens_used')}")
            print(f"   Preview: {data['analysis'][:200]}...")

            # Check if it mentions "unavailable" or "no data"
            if 'unavailable' in data['analysis'].lower() or 'no data' in data['analysis'].lower():
                print(f"\n⚠️  Stock data might not be available")
                print(f"   This could mean:")
                print(f"   • Finnhub API key not configured correctly")
                print(f"   • Workflow still using Yahoo Finance nodes")
                print(f"   • Markets are closed")
            else:
                print(f"\n🎉 Stock data successfully retrieved!")
        else:
            print(f"\n⚠️  No analysis in response")

    else:
        print(f"\n❌ Request failed: {response1.status_code}")
        print(f"   Response: {response1.text[:500]}")

except Exception as e:
    print(f"\n❌ Error: {e}")

# Test 2: With Telegram
print("\n" + "=" * 70)
print("📱 TEST 2: Fetch stock data + send to Telegram")
print("=" * 70)

proceed = input("\nSend test message to Telegram? (y/n): ").strip().lower()

if proceed == 'y':
    payload2 = {
        "symbols": "AAPL,MSFT,PRK",
        "send_to_telegram": True
    }

    print(f"\n📤 Request:")
    print(json.dumps(payload2, indent=2))

    try:
        response2 = requests.post(WEBHOOK_URL, json=payload2, timeout=120)

        print(f"\n📥 Response:")
        print(f"   Status: {response2.status_code}")

        if response2.status_code == 200:
            data = response2.json()
            print(f"\n✅ Success!")
            print(json.dumps(data, indent=2))

            if data.get('telegram_sent'):
                print(f"\n🎉 Telegram message sent!")
                print(f"   Message ID: {data.get('telegram_message_id')}")
                print(f"   Check your Telegram app!")
            else:
                print(f"\n⚠️  Telegram message not sent")
                print(f"   Check Telegram credentials in n8n")

        else:
            print(f"\n❌ Request failed: {response2.status_code}")
            print(f"   Response: {response2.text[:500]}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
else:
    print("\n⏭️  Skipping Telegram test")

# Test 3: Direct Finnhub API test
print("\n" + "=" * 70)
print("🔑 TEST 3: Direct Finnhub API test")
print("=" * 70)

finnhub_key = os.getenv('FINNHUB_API_KEY')

if finnhub_key:
    print(f"\n📡 Testing Finnhub API directly...")
    print(f"   API Key: {finnhub_key[:8]}...{finnhub_key[-8:]}")

    test_url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={finnhub_key}"

    try:
        finnhub_response = requests.get(test_url)

        if finnhub_response.status_code == 200:
            finnhub_data = finnhub_response.json()
            print(f"\n✅ Finnhub API is working!")
            print(f"\n📊 AAPL Stock Data:")
            print(f"   Current Price: ${finnhub_data.get('c')}")
            print(f"   Previous Close: ${finnhub_data.get('pc')}")
            print(f"   Change: ${finnhub_data.get('c') - finnhub_data.get('pc'):.2f}")
            print(f"   High: ${finnhub_data.get('h')}")
            print(f"   Low: ${finnhub_data.get('l')}")
        else:
            print(f"\n❌ Finnhub API failed: {finnhub_response.status_code}")
            print(f"   Response: {finnhub_response.text}")

            if finnhub_response.status_code == 401:
                print(f"\n⚠️  API key is invalid!")
                print(f"   1. Check your API key at: https://finnhub.io/dashboard")
                print(f"   2. Update .env file with correct key")
                print(f"   3. Update n8n credentials")

    except Exception as e:
        print(f"\n❌ Error: {e}")
else:
    print(f"\n⚠️  FINNHUB_API_KEY not found in .env")
    print(f"   Run: python3 setup_finnhub.py")

print("\n" + "=" * 70)
print("✅ Testing Complete!")
print("=" * 70)

print("\n📋 Summary:")
print("   • Workflow webhook: Tested")
print("   • Stock data retrieval: Check results above")
print("   • Telegram integration: Check results above")
print("   • Finnhub API: Check results above")

print("\n💡 Troubleshooting:")
print("   • If stock data is 'unavailable', check Finnhub credentials in n8n")
print("   • If Telegram doesn't send, verify Telegram credentials")
print("   • If workflow fails, check n8n execution logs")
print("   • Visit: http://100.82.85.95:5678/executions")

print("\n" + "=" * 70)
