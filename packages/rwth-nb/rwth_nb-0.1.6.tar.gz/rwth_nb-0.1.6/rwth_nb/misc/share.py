import os
import requests
import urllib

base_url = 'https://jupyter.rwth-aachen.de'
hub_api_url = f'{base_url}/hub/api'
shareable_prefix = 'shareable'


def get_hub_token(user, note=None, expires_in=None):
    token = os.environ['JUPYTERHUB_API_TOKEN']

    body = {}
    
    if expires_in:
        body['expires_in'] = expires_in

    if note:
        body['note'] = note

    r = requests.post(f'{hub_api_url}/users/{user}/tokens?', headers={
        'Authorization': 'Bearer ' + token
    }, json=body)
    r.raise_for_status()

    return r.json()['token']

def get_shareable_url(user=None, path=None, expires_in=24*60*60, note=''):
    if user is None:
        user = os.environ['JUPYTERHUB_USER']

    token = get_hub_token(user, note=f'{shareable_prefix}:{path}:{note}', expires_in=expires_in)

    path = urllib.parse.quote(path)

    return f'{base_url}/user/{user}/lab/tree/{path}?token={token}'


def get_shareable_tokens(user=None):
    if user is None:
        user = os.environ['JUPYTERHUB_USER']

    token = os.environ['JUPYTERHUB_API_TOKEN']

    r = requests.get(f'{hub_api_url}/users/{user}/tokens?', headers={
        'Authorization': 'Bearer ' + token
    })
    r.raise_for_status()
    
    tokens = []
    for token in r.json()['api_tokens']:
        if token['note'].startswith(shareable_prefix + ':'):
            tokens.append(token)

    return tokens

def revoke_shareable_token(token_id, user=None):
    if user is None:
        user = os.environ['JUPYTERHUB_USER']

    token = os.environ['JUPYTERHUB_API_TOKEN']

    r = requests.delete(f'{hub_api_url}/users/{user}/tokens/{token_id}', headers={
        'Authorization': 'Bearer ' + token
    })
    r.raise_for_status()
