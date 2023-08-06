import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError
from zephyr_sdk.exceptions.ZExceptions import MissingParametersError


# Create requirement tree
def create_requirement_tree(client, req_tree_spec):
    url = client.base_url + '/requirementtree/add'
    headers = {
        'Authorization': 'Bearer ' + client.token,
        'Content-Type': 'application/json'
    }

    # Validate request body
    error_list = []
    if 'projectId' not in req_tree_spec:
        error_list.append("projectId")

    if 'name' not in req_tree_spec:
        error_list.append("name")

    if 'description' not in req_tree_spec:
        error_list.append("description")

    if len(error_list) > 0:
        raise MissingParametersError(error_list)

    r = requests.post(url, headers=headers, json=req_tree_spec)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Get information on all requirement trees
def get_all_requirement_trees(client):
    url = client.base_url + '/requirementtree'
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Get the requirement trees in a specific project
def get_requirement_tree_with_ids(client, project_id, release_id):
    url = client.base_url + '/requirementtree?projectId=' + str(project_id)

    if release_id is not None:
        url += '&releaseid=' + str(release_id)

    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()

