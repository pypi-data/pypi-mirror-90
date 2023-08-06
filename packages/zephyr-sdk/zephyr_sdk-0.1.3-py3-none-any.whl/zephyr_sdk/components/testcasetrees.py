import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError


def get_testcase_tree_by_release_id(client, release_id):
    url = client.base_url + '/testcasetree/phases/' + str(release_id)
    headers = {
        "Authorization": "Bearer " + client.token
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())
    return r.json()
