import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError
from zephyr_sdk.exceptions.ZExceptions import MissingParametersError


def create_testcase(client, testcase_spec):
    url = client.base_url + '/testcase'
    headers = {
        "Authorization": "Bearer " + client.token,
        "Content-Type": "application/json"
    }

    # Validate request body
    error_list = []
    if 'name' not in testcase_spec['testcase']:
        error_list.append("testcase.name")
    if 'tcrCatalogTreeId' not in testcase_spec:
        error_list.append("tcrCatalogTreeId")

    if len(error_list) > 0:
        raise MissingParametersError(error_list)

    r = requests.post(url, headers=headers, json=testcase_spec)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


def map_testcase_to_requirements(client, map_spec):
    url = client.base_url + "/testcase/allocate/requirement"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + client.token
    }

    r = requests.post(url, headers=headers, json=map_spec)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())
    return r.json()
