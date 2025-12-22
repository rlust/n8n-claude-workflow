#!/usr/bin/env python3
"""Examine the exact input structure of the Telegram node"""
import json

with open('execution_detail.json', 'r') as f:
    exec_data = json.load(f)

run_data = exec_data.get('data', {}).get('resultData', {}).get('runData', {})

print("=" * 70)
print("🔍 Examining Telegram Node Input Structure")
print("=" * 70)

if 'Send to Telegram' in run_data:
    telegram_run = run_data['Send to Telegram'][0]

    print("\n📥 Full input structure:")
    print(json.dumps(telegram_run.get('data', {}), indent=2))

    print("\n" + "=" * 70)
    print("🔍 Examining If Node Output Structure (what feeds Telegram)")
    print("=" * 70)

if 'Send Telegram?' in run_data:
    if_run = run_data['Send Telegram?'][0]

    print("\n📤 If node output (true branch):")
    if 'data' in if_run and 'main' in if_run['data']:
        true_branch = if_run['data']['main'][0]
        print(json.dumps(true_branch, indent=2))

    print("\n" + "=" * 70)
    print("🔍 Comparing data structures")
    print("=" * 70)

    # Get If node output
    if_output = if_run['data']['main'][0][0]['json'] if if_run['data']['main'][0] else {}

    print(f"\n✅ Data from If node (true branch):")
    print(f"   chat_id: {if_output.get('chat_id')}")
    print(f"   send_telegram: {if_output.get('send_telegram')}")
    print(f"   analysis: {if_output.get('analysis', '')[:100]}...")

    # Get Telegram input
    telegram_input = telegram_run['data']['main'][0][0]['json'] if telegram_run['data']['main'][0] else {}

    print(f"\n❌ Data received by Telegram node:")
    print(f"   chat_id: {telegram_input.get('chat_id')}")
    print(f"   send_telegram: {telegram_input.get('send_telegram')}")
    print(f"   analysis: {telegram_input.get('analysis', '')[:100] if telegram_input.get('analysis') else 'None'}...")

    print(f"\n🔍 Full Telegram input JSON:")
    print(json.dumps(telegram_input, indent=2))
