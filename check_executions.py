#!/usr/bin/env python3
"""Check recent workflow executions"""
import requests
import json

# Load environment
N8N_API_KEY = ""
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('N8N_API_KEY='):
            N8N_API_KEY = line.split('=', 1)[1].strip()
            break

headers = {"X-N8N-API-KEY": N8N_API_KEY}
response = requests.get(
    "http://100.82.85.95:5678/api/v1/executions?limit=5",
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    executions = data.get('data', [])

    print("📋 Recent Executions")
    print("=" * 60)

    for i, exec_data in enumerate(executions, 1):
        print(f"\n{i}. Execution ID: {exec_data.get('id')}")
        print(f"   Workflow: {exec_data.get('workflowId')}")
        print(f"   Mode: {exec_data.get('mode')}")
        print(f"   Status: {'✅ Success' if exec_data.get('finished') else '❌ Failed'}")
        print(f"   Started: {exec_data.get('startedAt')}")

        # Check if it was triggered by cron or webhook
        mode = exec_data.get('mode', '')
        if 'trigger' in mode.lower():
            print(f"   Trigger: Cron/Scheduled")
        elif 'webhook' in mode.lower():
            print(f"   Trigger: Webhook")
        else:
            print(f"   Trigger: {mode}")

else:
    print(f"Error: {response.status_code}")
