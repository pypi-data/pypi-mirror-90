import os
import requests
from IPython.lib import kernel

base_url = 'https://jupyter.rwth-aachen.de'
hub_api_url = f'{base_url}/hub/api'

def get_current_path():
    token = os.environ['JUPYTERHUB_API_TOKEN']
    user = os.environ['JUPYTERHUB_USER']

    connection_file_path = kernel.get_connection_file()
    connection_file = os.path.basename(connection_file_path)
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]

    r = requests.request('GET', f'{base_url}/user/{user}/api/sessions', headers={
        'Authorization': f'Bearer {token}'
    })
    r.raise_for_status()
     
    for session in r.json():
        if session['kernel']['id'] == kernel_id:
            return session['notebook']['path']

def get_contents(path=None, user=None, token=None):
    if path is None:
        path = get_current_path()

    if user is None:
        user = os.environ['JUPYTERHUB_USER']
    
    if token is None:
        token = os.environ['JUPYTERHUB_API_TOKEN']

    r = requests.request('GET', f'{base_url}/user/{user}/api/contents/{path}', headers={
        'Authorization': 'Bearer ' + token
    })
    r.raise_for_status()

    return r.json()
