#!/usr/bin/env python3
"""Interactive Finnhub API setup script"""
import requests
import json
import os
from dotenv import load_dotenv
import sys

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

print("=" * 70)
print("🚀 Finnhub API Setup Wizard")
print("=" * 70)

print("\n📋 STEP 1: Sign up for Finnhub (FREE)")
print("   → Open this URL in your browser:")
print("   → https://finnhub.io/register")
print("\n   Fill in:")
print("   • Email address")
print("   • Password")
print("   • Click 'Sign Up'")
print("\n   Press ENTER when you've completed registration...")
input()

print("\n" + "=" * 70)
print("🔑 STEP 2: Get Your API Key")
print("=" * 70)
print("\n   → Open this URL in your browser:")
print("   → https://finnhub.io/dashboard")
print("\n   You should see your API Key displayed on the dashboard")
print("   It looks something like: ctodfupr01qretc7a2dgctodfupr01qretc7a2e0")
print("\n   Copy your API key to clipboard")
print("   Press ENTER when ready...")
input()

print("\n" + "=" * 70)
print("🔐 STEP 3: Enter Your API Key")
print("=" * 70)
finnhub_api_key = input("\nPaste your Finnhub API key here: ").strip()

if not finnhub_api_key:
    print("❌ No API key provided. Exiting.")
    sys.exit(1)

print(f"\n✅ API Key received (length: {len(finnhub_api_key)} characters)")

# Test the API key
print("\n🧪 Testing API key...")
test_response = requests.get(
    f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={finnhub_api_key}"
)

if test_response.status_code == 200:
    data = test_response.json()
    if 'c' in data:
        print(f"✅ API key is VALID!")
        print(f"   Test: AAPL current price = ${data['c']}")
    else:
        print(f"⚠️  API returned unexpected format: {data}")
elif test_response.status_code == 401:
    print(f"❌ API key is INVALID. Please check and try again.")
    print(f"   Response: {test_response.text}")
    sys.exit(1)
else:
    print(f"⚠️  Unexpected response: {test_response.status_code}")
    print(f"   {test_response.text}")

print("\n" + "=" * 70)
print("📝 STEP 4: Add Credentials to n8n")
print("=" * 70)

# Check if Finnhub credential type exists
print("\n🔍 Checking n8n credential types...")

# Get list of credentials
creds_response = requests.get(
    f"{N8N_URL}/api/v1/credentials",
    headers=headers
)

if creds_response.status_code == 200:
    credentials = creds_response.json()
    print(f"✅ Found {len(credentials)} existing credentials in n8n")

    # Check if finnhubApi already exists
    finnhub_creds = [c for c in credentials if c.get('type') == 'finnhubApi']

    if finnhub_creds:
        print(f"\n⚠️  Found {len(finnhub_creds)} existing Finnhub credential(s)")
        for cred in finnhub_creds:
            print(f"   • {cred.get('name')} (ID: {cred.get('id')})")

        update = input("\n   Update existing credential? (y/n): ").strip().lower()

        if update == 'y':
            cred_id = finnhub_creds[0]['id']

            # Update existing credential
            update_payload = {
                'name': finnhub_creds[0]['name'],
                'type': 'finnhubApi',
                'data': {
                    'apiKey': finnhub_api_key
                }
            }

            update_response = requests.patch(
                f"{N8N_URL}/api/v1/credentials/{cred_id}",
                headers=headers,
                json=update_payload
            )

            if update_response.status_code == 200:
                print(f"\n✅ Updated Finnhub credential successfully!")
            else:
                print(f"\n❌ Failed to update: {update_response.status_code}")
                print(f"   {update_response.text}")
        else:
            print("\n⚠️  Skipping credential update")
    else:
        print("\n📝 Creating new Finnhub credential...")

        # Create new credential
        create_payload = {
            'name': 'finnhubApi',
            'type': 'finnhubApi',
            'data': {
                'apiKey': finnhub_api_key
            }
        }

        create_response = requests.post(
            f"{N8N_URL}/api/v1/credentials",
            headers=headers,
            json=create_payload
        )

        if create_response.status_code in [200, 201]:
            print(f"✅ Created Finnhub credential successfully!")
            created = create_response.json()
            print(f"   Credential ID: {created.get('id')}")
        else:
            print(f"❌ Failed to create: {create_response.status_code}")
            print(f"   {create_response.text}")
            print(f"\n   Manual setup required:")
            print(f"   1. Go to: {N8N_URL}/credentials")
            print(f"   2. Click 'Add Credential'")
            print(f"   3. Search for 'Finnhub API'")
            print(f"   4. Name: finnhubApi")
            print(f"   5. API Key: {finnhub_api_key}")
            print(f"   6. Click 'Save'")

else:
    print(f"⚠️  Could not fetch credentials: {creds_response.status_code}")
    print(f"\n   Manual setup required:")
    print(f"   1. Go to: {N8N_URL}/credentials")
    print(f"   2. Click 'Add Credential'")
    print(f"   3. Search for 'Finnhub API'")
    print(f"   4. Name: finnhubApi")
    print(f"   5. API Key: {finnhub_api_key}")
    print(f"   6. Click 'Save'")

# Save API key to .env
print("\n💾 Saving API key to .env file...")
with open('.env', 'a') as f:
    f.write(f"\nFINNHUB_API_KEY={finnhub_api_key}")
print("✅ Saved to .env")

print("\n" + "=" * 70)
print("🎯 STEP 5: Activate Workflow")
print("=" * 70)

workflow_id = os.getenv('WORKFLOW_ID_FINNHUB')
if workflow_id:
    print(f"\n🔄 Activating workflow: {workflow_id}")

    # Get workflow
    workflow_response = requests.get(
        f"{N8N_URL}/api/v1/workflows/{workflow_id}",
        headers=headers
    )

    if workflow_response.status_code == 200:
        workflow = workflow_response.json()

        # Activate it
        activate_payload = {
            'active': True
        }

        activate_response = requests.patch(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=headers,
            json=activate_payload
        )

        if activate_response.status_code == 200:
            print("✅ Workflow activated successfully!")
        else:
            print(f"⚠️  Could not activate: {activate_response.status_code}")
            print(f"   Activate manually at: {N8N_URL}/workflow/{workflow_id}")
    else:
        print(f"⚠️  Could not get workflow: {workflow_response.status_code}")
else:
    print("\n⚠️  Workflow ID not found in .env")
    print(f"   Activate manually at: {N8N_URL}/workflows")

print("\n" + "=" * 70)
print("✅ Setup Complete!")
print("=" * 70)

print("\n📋 Summary:")
print(f"   • API Key: {finnhub_api_key[:8]}...{finnhub_api_key[-8:]}")
print(f"   • Credentials: Configured in n8n")
print(f"   • Workflow: Ready to test")

print("\n🧪 Next Step: Test the workflow")
print("   Run: python3 test_finnhub_workflow.py")

print("\n" + "=" * 70)
