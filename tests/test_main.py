import os
import subprocess
import requests
import pytest
from main import (
    get_inputs,
    get_access_token_and_instance_url,
    create_session_environment,
    revoke_salesforce_grant,
    delete_session_environment
)

def test_get_inputs(monkeypatch):
    monkeypatch.setenv('INPUT_SFDX_AUTH_URL', 'test_sfdx_auth_url')
    monkeypatch.setenv('INPUT_GITHUB_TOKEN', 'test_github_token')
    sfdx_auth_url, github_token = get_inputs()
    assert sfdx_auth_url == 'test_sfdx_auth_url'
    assert github_token == 'test_github_token'

def test_get_access_token_and_instance_url(mocker):
    mocker.patch('subprocess.run', return_value=subprocess.CompletedProcess(
        args=['d2x', 'auth', 'sf', 'url', 'test_sfdx_auth_url'],
        returncode=0,
        stdout='access_token=test_access_token\ninstance_url=test_instance_url'
    ))
    access_token, instance_url = get_access_token_and_instance_url('test_sfdx_auth_url')
    assert access_token == 'test_access_token'
    assert instance_url == 'test_instance_url'

def test_create_session_environment(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'id': 'test_environment_id'}
    mocker.patch('requests.post', return_value=mock_response)
    github_token = 'test_github_token'
    response = create_session_environment(github_token)
    assert response['id'] == 'test_environment_id'

def test_revoke_salesforce_grant(mocker):
    mock_response = mocker.Mock()
    mocker.patch('requests.post', return_value=mock_response)
    access_token = 'test_access_token'
    instance_url = 'test_instance_url'
    revoke_salesforce_grant(access_token, instance_url)
    mocker.patch('requests.post').assert_called_once_with(
        f'{instance_url}/services/oauth2/revoke',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    )

def test_delete_session_environment(mocker):
    mock_response = mocker.Mock()
    mocker.patch('requests.delete', return_value=mock_response)
    github_token = 'test_github_token'
    delete_session_environment(github_token)
    mocker.patch('requests.delete').assert_called_once_with(
        'https://api.github.com/repos/githubnext/workspace-blank/environments',
        headers={
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
