import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError
from zephyr_sdk.exceptions.ZExceptions import MissingParametersError


# Create a requirement.
def create_requirement(client, requirement_spec):
    url = client.base_url + '/requirement/'
    headers = {
        'Authorization': 'Bearer ' + client.token,
        'Content-Type': 'application/json'
    }

    # Validate request body
    error_list = []
    if 'requirementTreeId' not in requirement_spec:
        error_list.append("requirementTreeId")
    if 'name' not in requirement_spec:
        error_list.append("name")

    if len(error_list) > 0:
        raise MissingParametersError(error_list)

    r = requests.post(url, headers=headers, json=requirement_spec)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Delete a requirement by requirement id
def delete_requirement(client, req_id):
    url = client.base_url + '/requirement/' + str(req_id)
    headers = {
        'Authorization': 'Bearer ' + client.token,
    }
    r = requests.delete(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Get a list of requirements from the requirement tree.
def get_requirements(client, req_tree_id):
    url = client.base_url + '/requirement?requirementtreeid=' + str(req_tree_id)
    headers = {
        'Authorization': 'Bearer ' + client.token,
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Update a requirement when given the id.
def update_requirement(client, req_id, requirement_spec):
    url = client.base_url + '/requirement/' + req_id
    headers = {
        'Authorization': 'Bearer ' + client.token,
        'Content-Type': 'application/json'
    }
    r = requests.put(url, headers=headers, json=requirement_spec)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()
