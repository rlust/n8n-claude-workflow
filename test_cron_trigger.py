#!/usr/bin/env python3
"""Manually test the cron trigger path"""
import requests
import json
import time

# Load environment
N8N_API_KEY = ""
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('N8N_API_KEY='):
            N8N_API_KEY = line.split('=', 1)[1].strip()
            break

N8N_URL = "http://100.82.85.95:5678"
WORKFLOW_ID = "B96iHmEjsX6Yo3IM"
headers = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}

print("🧪 Testing scheduled workflow (Cron trigger path)")
print("=" * 60)

# Trigger manual execution
print("\n1. Triggering workflow execution...")
payload = {
    "workflowId": WORKFLOW_ID
}

response = requests.post(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}/execute",
    headers=headers,
    json=payload
)

if response.status_code in [200, 201]:
    result = response.json()
    execution_id = result.get('data', {}).get('executionId') or result.get('executionId')

    print(f"   ✅ Workflow triggered!")
    print(f"   Execution ID: {execution_id}")

    # Wait a bit for execution to complete
    print("\n2. Waiting for execution to complete...")
    time.sleep(5)

    # Get execution result
    print("\n3. Getting execution result...")
    exec_response = requests.get(
        f"{N8N_URL}/api/v1/executions/{execution_id}",
        headers=headers
    )

    if exec_response.status_code == 200:
        exec_data = exec_response.json().get('data', exec_response.json())

        status = exec_data.get('finished')
        mode = exec_data.get('mode')

        print(f"   Status: {'✅ Finished' if status else '❌ Failed'}")
        print(f"   Mode: {mode}")

        if not status:
            # Show error if any
            error_message = exec_data.get('data', {}).get('resultData', {}).get('error')
            if error_message:
                print(f"\n   ❌ Error: {error_message}")

            # Check for node errors
            if 'data' in exec_data and 'resultData' in exec_data['data']:
                result_data = exec_data['data']['resultData']
                if 'runData' in result_data:
                    print("\n   📋 Node execution status:")
                    for node_name, node_data in result_data['runData'].items():
                        if isinstance(node_data, list) and len(node_data) > 0:
                            node_run = node_data[0]
                            if 'error' in node_run:
                                print(f"      ❌ {node_name}: {node_run['error'].get('message', 'Unknown error')}")
                            else:
                                print(f"      ✅ {node_name}")
        else:
            print("\n   ✅ Workflow executed successfully!")

            # Try to get the analysis output
            if 'data' in exec_data and 'resultData' in exec_data['data']:
                result_data = exec_data['data']['resultData']
                if 'runData' in result_data:
                    # Check if Telegram was sent
                    if 'Send to Telegram' in result_data['runData']:
                        print("   📱 Telegram message sent!")

                    # Show stock symbols analyzed
                    if 'Merge Triggers' in result_data['runData']:
                        merge_data = result_data['runData']['Merge Triggers'][0]
                        if 'data' in merge_data and 'main' in merge_data['data']:
                            items = merge_data['data']['main'][0]
                            if items and len(items) > 0:
                                symbols = []
                                for item in items:
                                    if 'json' in item and 'symbol1' in item['json']:
                                        symbols.append(item['json']['symbol1'])
                                        symbols.append(item['json']['symbol2'])
                                if symbols:
                                    print(f"   📊 Stocks analyzed: {', '.join(set(symbols))}")
    else:
        print(f"   ❌ Could not get execution result: {exec_response.status_code}")

else:
    print(f"   ❌ Failed to trigger workflow: {response.status_code}")
    print(f"   Response: {response.text}")
