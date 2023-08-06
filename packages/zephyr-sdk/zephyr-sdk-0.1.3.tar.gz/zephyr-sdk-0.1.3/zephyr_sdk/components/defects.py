import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError
from zephyr_sdk.exceptions.ZExceptions import MissingParametersError


def create_defect(client, defect_spec):
    url = client.base_url + '/defect'
    headers = {
        "Authorization": "Bearer " + client.token,
        "Content-Type": "application/json"
    }

    # Validate the request body
    error_list = []
    if 'projectId' not in defect_spec:
        error_list.append("projectId")
    if 'product' not in defect_spec:
        error_list.append("product")

    if len(error_list) > 0:
        raise MissingParametersError(error_list)

    r = requests.post(url, headers=headers, json=defect_spec)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()
