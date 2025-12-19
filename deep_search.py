#!/usr/bin/env python3
import requests
import json

N8N_API_KEY = ''
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('N8N_API_KEY='):
            N8N_API_KEY = line.split('=', 1)[1].strip()
            break

headers = {'X-N8N-API-KEY': N8N_API_KEY}
response = requests.get('http://100.82.85.95:5678/api/v1/workflows/B96iHmEjsX6Yo3IM', headers=headers)

if response.status_code == 200:
    data = response.json()
    workflow = data.get('data', data)

    workflow_str = json.dumps(workflow)

    # Count references
    search_term = "$('Extract Params')"
    count = workflow_str.count(search_term)
    print(f'Total {search_term} references found: {count}\n')

    if count > 0:
        print('Searching in all nodes...\n')
        for node in workflow.get('nodes', []):
            node_str = json.dumps(node)
            if search_term in node_str:
                print(f'❌ Found in: {node.get("name")} ({node.get("type")})')
                # Show the full parameters
                params_str = json.dumps(node.get('parameters', {}))
                if 'Extract Params' in params_str:
                    # Find and print the specific expression
                    for key, value in node.get('parameters', {}).items():
                        value_str = json.dumps(value)
                        if 'Extract Params' in value_str:
                            print(f'   Parameter: {key}')
                            print(f'   Contains: {value_str[:200]}...')
                print()
else:
    print(f'Error: {response.status_code}')
