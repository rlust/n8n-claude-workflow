#!/usr/bin/env python3
"""Check actual execution data to see what Telegram node receives"""
import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
WEBHOOK_URL = os.getenv('WEBHOOK_URL_STOCK_TELEGRAM_V3')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("🧪 Step-by-step execution data inspection\n")
print("=" * 70)

# Step 1: Trigger workflow
print("\n📤 STEP 1: Triggering workflow...")
payload = {
    "symbols": "AAPL,MSFT,GOOGL",
    "send_to_telegram": True
}
print(f"   Payload: {json.dumps(payload, indent=2)}")

webhook_response = requests.post(WEBHOOK_URL, json=payload, timeout=120)
print(f"   Status: {webhook_response.status_code}")
print(f"   Response: {json.dumps(webhook_response.json(), indent=2)}")

# Step 2: Wait briefly for execution to complete
print("\n⏳ STEP 2: Waiting 3 seconds for execution to complete...")
time.sleep(3)

# Step 3: Get most recent execution
print("\n📥 STEP 3: Fetching execution details...")
exec_list_response = requests.get(
    f"{N8N_URL}/api/v1/executions?limit=1",
    headers=headers
)

if exec_list_response.status_code != 200:
    print(f"   ❌ Failed to get executions: {exec_list_response.status_code}")
    print(f"   Response: {exec_list_response.text}")
    exit(1)

executions = exec_list_response.json().get('data', [])
if not executions:
    print("   ❌ No executions found!")
    exit(1)

exec_id = executions[0]['id']
print(f"   ✅ Found execution: {exec_id}")
print(f"   Status: {executions[0].get('status')}")
print(f"   Finished: {executions[0].get('finished')}")

# Step 4: Get detailed execution data with includeData parameter
print("\n🔍 STEP 4: Getting detailed execution data...")
exec_detail_response = requests.get(
    f"{N8N_URL}/api/v1/executions/{exec_id}?includeData=true",
    headers=headers
)

if exec_detail_response.status_code != 200:
    print(f"   ❌ Failed to get execution details: {exec_detail_response.status_code}")
    print(f"   Response: {exec_detail_response.text}")
    exit(1)

execution_data = exec_detail_response.json()
print(f"   ✅ Retrieved execution data")

# Save full execution data for inspection
with open('execution_detail.json', 'w') as f:
    json.dump(execution_data, f, indent=2)
print(f"   💾 Saved full data to execution_detail.json")

# Step 5: Analyze node execution data
print("\n📊 STEP 5: Analyzing node execution data...")

result_data = execution_data.get('data', {}).get('resultData', {})
run_data = result_data.get('runData', {})

print(f"\n   Nodes that executed: {list(run_data.keys())}")

# Check if Telegram node executed
if 'Send to Telegram' in run_data:
    print("\n   ✅ 'Send to Telegram' node executed")

    telegram_run = run_data['Send to Telegram']
    print(f"   Number of runs: {len(telegram_run)}")

    if telegram_run:
        # Get input data
        first_run = telegram_run[0]
        print(f"\n   📥 Telegram Node INPUT:")

        if 'data' in first_run and 'main' in first_run['data']:
            input_items = first_run['data']['main'][0]
            print(f"   Number of input items: {len(input_items)}")

            for i, item in enumerate(input_items):
                item_json = item.get('json', {})
                print(f"\n   Item {i}:")
                print(f"      chat_id: {item_json.get('chat_id')}")
                print(f"      send_telegram: {item_json.get('send_telegram')}")
                analysis = item_json.get('analysis', '')
                print(f"      analysis length: {len(analysis)} chars")
                print(f"      analysis preview: {analysis[:200]}...")

        # Get output data
        print(f"\n   📤 Telegram Node OUTPUT:")
        if 'data' in first_run and 'main' in first_run['data']:
            # Check if there's output
            if len(first_run['data']['main']) > 1:
                output_items = first_run['data']['main'][1]
                for i, item in enumerate(output_items):
                    item_json = item.get('json', {})
                    print(f"\n   Item {i}:")
                    print(f"      message_id: {item_json.get('message_id')}")
                    print(f"      Full output: {json.dumps(item_json, indent=6)}")
            else:
                print("   ⚠️ No output data from Telegram node")

        # Check for errors
        if 'error' in first_run:
            print(f"\n   ❌ ERROR in Telegram node:")
            print(f"   {json.dumps(first_run['error'], indent=6)}")
else:
    print("\n   ❌ 'Send to Telegram' node did NOT execute!")
    print(f"   Available nodes: {list(run_data.keys())}")

# Step 6: Check Extract Analysis node output
print("\n" + "=" * 70)
print("📊 STEP 6: Checking 'Extract Analysis' node output...")

if 'Extract Analysis' in run_data:
    extract_run = run_data['Extract Analysis'][0]
    if 'data' in extract_run and 'main' in extract_run['data']:
        output_items = extract_run['data']['main'][0]
        print(f"   Number of output items: {len(output_items)}")

        for i, item in enumerate(output_items):
            item_json = item.get('json', {})
            print(f"\n   Item {i}:")
            print(f"      analysis: {item_json.get('analysis', '')[:200]}...")
            print(f"      chat_id: {item_json.get('chat_id')}")
            print(f"      send_telegram: {item_json.get('send_telegram')}")
            print(f"      tokens: {item_json.get('tokens')}")

# Step 7: Check If node
print("\n" + "=" * 70)
print("📊 STEP 7: Checking 'Send Telegram?' (If) node...")

if 'Send Telegram?' in run_data:
    if_run = run_data['Send Telegram?'][0]
    if 'data' in if_run and 'main' in if_run['data']:
        # If node has two outputs: [0] = true branch, [1] = false branch
        true_branch = if_run['data']['main'][0] if len(if_run['data']['main']) > 0 else []
        false_branch = if_run['data']['main'][1] if len(if_run['data']['main']) > 1 else []

        print(f"   True branch items: {len(true_branch)}")
        print(f"   False branch items: {len(false_branch)}")

        if true_branch:
            print(f"\n   ✅ Condition evaluated to TRUE")
            for i, item in enumerate(true_branch):
                item_json = item.get('json', {})
                print(f"   Item {i} passed to Telegram:")
                print(f"      send_telegram: {item_json.get('send_telegram')}")
                print(f"      chat_id: {item_json.get('chat_id')}")
        else:
            print(f"\n   ❌ Condition evaluated to FALSE - no data sent to Telegram!")

print("\n" + "=" * 70)
print("✅ Analysis complete! Check execution_detail.json for full data.")
