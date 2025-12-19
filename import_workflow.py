#!/usr/bin/env python3
"""
Import and activate n8n workflow via API
"""
import requests
import json
import sys
import os

# Configuration
N8N_URL = os.getenv("N8N_URL", "http://100.82.85.95:5678")
API_KEY = os.getenv("N8N_API_KEY", "")
WORKFLOW_FILE = "n8n-workflows/examples/claude-stock-to-telegram.json"

if not API_KEY:
    print("Error: N8N_API_KEY environment variable not set")
    sys.exit(1)

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text):
    print(f"{Colors.CYAN}ℹ {text}{Colors.RESET}")


def load_workflow():
    """Load workflow from JSON file"""
    print_info(f"Loading workflow from {WORKFLOW_FILE}")
    try:
        with open(WORKFLOW_FILE, 'r') as f:
            workflow = json.load(f)
        print_success(f"Loaded workflow: {workflow.get('name', 'Unknown')}")
        return workflow
    except FileNotFoundError:
        print_error(f"Workflow file not found: {WORKFLOW_FILE}")
        return None
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in workflow file: {e}")
        return None


def get_headers():
    """Get API headers with authentication"""
    return {
        "X-N8N-API-KEY": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def check_existing_workflow(workflow_name):
    """Check if workflow already exists"""
    print_info("Checking for existing workflows...")

    try:
        response = requests.get(
            f"{N8N_URL}/api/v1/workflows",
            headers=get_headers(),
            timeout=10
        )

        if response.status_code == 200:
            workflows = response.json().get('data', [])
            for wf in workflows:
                if wf.get('name') == workflow_name:
                    print_info(f"Found existing workflow: {wf.get('name')} (ID: {wf.get('id')})")
                    return wf.get('id')
            print_info("No existing workflow found with this name")
            return None
        else:
            print_error(f"Failed to list workflows: {response.status_code}")
            return None

    except Exception as e:
        print_error(f"Error checking existing workflows: {e}")
        return None


def import_workflow(workflow_data):
    """Import workflow via n8n API"""
    workflow_name = workflow_data.get('name', 'Unknown')
    print_info(f"Importing workflow: {workflow_name}")

    # Check if workflow already exists
    existing_id = check_existing_workflow(workflow_name)

    if existing_id:
        print_info("Updating existing workflow...")
        method = "PUT"
        url = f"{N8N_URL}/api/v1/workflows/{existing_id}"
    else:
        print_info("Creating new workflow...")
        method = "POST"
        url = f"{N8N_URL}/api/v1/workflows"

    # Prepare workflow data
    workflow_payload = {
        "name": workflow_data.get("name"),
        "nodes": workflow_data.get("nodes"),
        "connections": workflow_data.get("connections"),
        "settings": workflow_data.get("settings", {}),
        "staticData": workflow_data.get("staticData")
    }

    # Only set these fields for new workflows
    if not existing_id:
        workflow_payload["active"] = False
        workflow_payload["tags"] = workflow_data.get("tags", [])

    try:
        if method == "POST":
            response = requests.post(url, headers=get_headers(), json=workflow_payload, timeout=30)
        else:
            response = requests.put(url, headers=get_headers(), json=workflow_payload, timeout=30)

        if response.status_code in [200, 201]:
            result = response.json()
            workflow_id = result.get('data', {}).get('id') or result.get('id')
            print_success(f"Workflow imported successfully! ID: {workflow_id}")
            return workflow_id
        else:
            print_error(f"Failed to import workflow: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None

    except Exception as e:
        print_error(f"Error importing workflow: {e}")
        return None


def activate_workflow(workflow_id):
    """Activate the workflow"""
    print_info(f"Activating workflow {workflow_id}...")

    try:
        # First, get the current workflow
        get_response = requests.get(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=get_headers(),
            timeout=10
        )

        if get_response.status_code != 200:
            print_error(f"Failed to get workflow: {get_response.status_code}")
            return False

        response_data = get_response.json()
        # n8n API might return data directly or wrapped in 'data' field
        if 'data' in response_data:
            current_workflow = response_data['data']
        else:
            current_workflow = response_data

        print_info(f"Current workflow active status: {current_workflow.get('active')}")

        # Update with active=True
        update_payload = {
            "name": current_workflow.get("name"),
            "nodes": current_workflow.get("nodes"),
            "connections": current_workflow.get("connections"),
            "settings": current_workflow.get("settings", {}),
            "staticData": current_workflow.get("staticData"),
            "active": True
        }

        response = requests.put(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=get_headers(),
            json=update_payload,
            timeout=10
        )

        if response.status_code == 200:
            print_success("Workflow activated successfully!")
            return True
        else:
            print_error(f"Failed to activate workflow: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False

    except Exception as e:
        print_error(f"Error activating workflow: {e}")
        return False


def get_workflow_info(workflow_id):
    """Get workflow information including webhook URL"""
    print_info("Getting workflow information...")

    try:
        response = requests.get(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=get_headers(),
            timeout=10
        )

        if response.status_code == 200:
            response_data = response.json()
            # n8n API might return data directly or wrapped in 'data' field
            if 'data' in response_data:
                workflow = response_data['data']
            else:
                workflow = response_data

            print_success(f"Workflow name: {workflow.get('name')}")
            print_success(f"Workflow ID: {workflow.get('id')}")
            print_success(f"Active: {workflow.get('active')}")

            # Try to find webhook URL
            nodes = workflow.get('nodes', [])
            for node in nodes:
                if node.get('type') == 'n8n-nodes-base.webhook':
                    webhook_path = node.get('parameters', {}).get('path', '')
                    webhook_url = f"{N8N_URL}/webhook/{webhook_path}"
                    print_success(f"Webhook URL: {webhook_url}")
                    return webhook_url

            return None
        else:
            print_error(f"Failed to get workflow info: {response.status_code}")
            return None

    except Exception as e:
        print_error(f"Error getting workflow info: {e}")
        return None


def main():
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}n8n Workflow Importer{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")

    # Load workflow
    workflow = load_workflow()
    if not workflow:
        sys.exit(1)

    # Import workflow
    workflow_id = import_workflow(workflow)
    if not workflow_id:
        sys.exit(1)

    # Activate workflow
    if not activate_workflow(workflow_id):
        print_error("Failed to activate workflow, but it was imported")

    # Get workflow info
    webhook_url = get_workflow_info(workflow_id)

    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Workflow setup complete!{Colors.RESET}\n")

    if webhook_url:
        print(f"{Colors.CYAN}Test it with:{Colors.RESET}")
        print(f'curl -X POST {webhook_url} \\')
        print(f'  -H "Content-Type: application/json" \\')
        print(f'  -d \'{{"symbols": "AAPL,MSFT", "send_to_telegram": false}}\'')
        print()


if __name__ == "__main__":
    main()
