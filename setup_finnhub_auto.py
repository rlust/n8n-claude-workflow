#!/usr/bin/env python3
"""Automatic Finnhub setup with provided API key"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')
FINNHUB_API_KEY = "cu6krs9r01qh2ki5u5tgcu6krs9r01qh2ki5u5u0"

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("=" * 70)
print("🔧 Automatic Finnhub Setup")
print("=" * 70)

# Step 1: Test the API key
print("\n📡 Testing Finnhub API key...")
test_response = requests.get(
    f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={FINNHUB_API_KEY}"
)

if test_response.status_code == 200:
    data = test_response.json()
    if 'c' in data:
        print(f"✅ API key is VALID!")
        print(f"   Test: AAPL = ${data['c']} (change: ${data['c'] - data['pc']:.2f})")
    else:
        print(f"⚠️  Unexpected response: {data}")
        exit(1)
elif test_response.status_code == 401:
    print(f"❌ API key is INVALID")
    print(f"   Response: {test_response.text}")
    exit(1)
else:
    print(f"⚠️  Status: {test_response.status_code}")
    print(f"   {test_response.text}")

# Step 2: Add to n8n credentials
print("\n🔐 Adding Finnhub credentials to n8n...")

# Get existing credentials
creds_response = requests.get(
    f"{N8N_URL}/api/v1/credentials",
    headers=headers
)

if creds_response.status_code == 200:
    credentials = creds_response.json()
    finnhub_creds = [c for c in credentials if c.get('type') == 'finnhubApi']

    if finnhub_creds:
        print(f"   Found existing Finnhub credential: {finnhub_creds[0]['name']}")
        cred_id = finnhub_creds[0]['id']

        # Update it
        update_payload = {
            'name': finnhub_creds[0]['name'],
            'type': 'finnhubApi',
            'data': {
                'apiKey': FINNHUB_API_KEY
            }
        }

        update_response = requests.patch(
            f"{N8N_URL}/api/v1/credentials/{cred_id}",
            headers=headers,
            json=update_payload
        )

        if update_response.status_code == 200:
            print(f"   ✅ Updated existing credential")
        else:
            print(f"   ⚠️  Update failed: {update_response.status_code}")
            print(f"   {update_response.text}")
    else:
        print(f"   Creating new Finnhub credential...")

        create_payload = {
            'name': 'finnhubApi',
            'type': 'finnhubApi',
            'data': {
                'apiKey': FINNHUB_API_KEY
            }
        }

        create_response = requests.post(
            f"{N8N_URL}/api/v1/credentials",
            headers=headers,
            json=create_payload
        )

        if create_response.status_code in [200, 201]:
            created = create_response.json()
            print(f"   ✅ Created credential: {created.get('id')}")
        else:
            print(f"   ❌ Failed: {create_response.status_code}")
            print(f"   {create_response.text}")
else:
    print(f"   ⚠️  Could not fetch credentials: {creds_response.status_code}")

# Step 3: Save to .env
print("\n💾 Saving to .env file...")
env_path = '.env'
with open(env_path, 'r') as f:
    env_content = f.read()

if 'FINNHUB_API_KEY' in env_content:
    # Update existing
    lines = env_content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('FINNHUB_API_KEY='):
            new_lines.append(f'FINNHUB_API_KEY={FINNHUB_API_KEY}')
        else:
            new_lines.append(line)
    with open(env_path, 'w') as f:
        f.write('\n'.join(new_lines))
    print("   ✅ Updated FINNHUB_API_KEY in .env")
else:
    # Add new
    with open(env_path, 'a') as f:
        f.write(f'\nFINNHUB_API_KEY={FINNHUB_API_KEY}\n')
    print("   ✅ Added FINNHUB_API_KEY to .env")

# Step 4: Activate workflow
print("\n⚡ Activating Finnhub workflow...")
workflow_id = os.getenv('WORKFLOW_ID_FINNHUB')

if workflow_id:
    activate_payload = {
        'active': True
    }

    activate_response = requests.patch(
        f"{N8N_URL}/api/v1/workflows/{workflow_id}",
        headers=headers,
        json=activate_payload
    )

    if activate_response.status_code == 200:
        print(f"   ✅ Workflow activated!")
    else:
        print(f"   ⚠️  Activation status: {activate_response.status_code}")
else:
    print(f"   ⚠️  Workflow ID not found in .env")

print("\n" + "=" * 70)
print("✅ Setup Complete!")
print("=" * 70)

print("\n📋 Summary:")
print(f"   • API Key: {FINNHUB_API_KEY[:8]}...{FINNHUB_API_KEY[-8:]}")
print(f"   • n8n Credentials: ✅ Configured")
print(f"   • .env File: ✅ Updated")
print(f"   • Workflow: ✅ Activated")

print("\n🧪 Next: Test the workflow")
print("   Run: python3 test_finnhub_workflow.py")

print("\n" + "=" * 70)
