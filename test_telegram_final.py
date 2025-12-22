#!/usr/bin/env python3
"""Final test - verify telegram_message_id is now captured"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv('WEBHOOK_URL_STOCK_TELEGRAM_V3')

print("🧪 Final Test: Verify Telegram message_id fix\n")
print("=" * 70)

payload = {
    "symbols": "AAPL,MSFT",
    "send_to_telegram": True  # ENABLE Telegram
}

print(f"📤 Sending request:")
print(f"   Symbols: {payload['symbols']}")
print(f"   Send to Telegram: {payload['send_to_telegram']}")

try:
    response = requests.post(WEBHOOK_URL, json=payload, timeout=120)

    if response.status_code == 200:
        data = response.json()

        print(f"\n✅ Workflow executed successfully!")
        print(f"\n📊 Response data:")
        print(json.dumps(data, indent=2))

        print(f"\n" + "=" * 70)
        print(f"🔍 Telegram Status:")
        print(f"   telegram_sent: {data.get('telegram_sent')}")
        print(f"   telegram_message_id: {data.get('telegram_message_id')}")

        if data.get('telegram_message_id'):
            print(f"\n🎉 SUCCESS! Message ID captured: {data.get('telegram_message_id')}")
            print(f"✅ The fix worked - Telegram is now fully functional!")
        else:
            print(f"\n⚠️  Message ID is still None")
            print(f"   Check if Telegram actually sent the message")

    else:
        print(f"❌ Request failed with status: {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
