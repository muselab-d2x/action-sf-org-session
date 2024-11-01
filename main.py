import os
import subprocess
import requests

def get_inputs():
    sfdx_auth_url = os.getenv('INPUT_SFDX_AUTH_URL')
    github_token = os.getenv('INPUT_GITHUB_TOKEN')
    return sfdx_auth_url, github_token

def get_access_token_and_instance_url(sfdx_auth_url):
    result = subprocess.run(['d2x', 'auth', 'sf', 'url', sfdx_auth_url], capture_output=True, text=True)
    output = result.stdout.strip().split('\n')
    access_token = output[0].split('=')[1].strip()
    instance_url = output[1].split('=')[1].strip()
    return access_token, instance_url

def create_session_environment(github_token):
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.post('https://api.github.com/repos/githubnext/workspace-blank/environments', headers=headers)
    response.raise_for_status()
    return response.json()

def revoke_salesforce_grant(access_token, instance_url):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f'{instance_url}/services/oauth2/revoke', headers=headers)
    response.raise_for_status()

def delete_session_environment(github_token):
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.delete('https://api.github.com/repos/githubnext/workspace-blank/environments', headers=headers)
    response.raise_for_status()

def main():
    sfdx_auth_url, github_token = get_inputs()
    access_token, instance_url = get_access_token_and_instance_url(sfdx_auth_url)
    create_session_environment(github_token)
    # Add logic to check for a flag to end the session
    # If the flag is set, revoke the Salesforce grant and delete the session environment
    revoke_salesforce_grant(access_token, instance_url)
    delete_session_environment(github_token)

if __name__ == '__main__':
    main()
