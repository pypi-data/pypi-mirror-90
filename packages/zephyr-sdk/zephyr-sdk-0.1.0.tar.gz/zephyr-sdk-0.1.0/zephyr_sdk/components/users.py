import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError


# Get all the currently logged in users.
def get_current_logged_in_users(client):
    url = client.base_url + '/user/current'
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()
