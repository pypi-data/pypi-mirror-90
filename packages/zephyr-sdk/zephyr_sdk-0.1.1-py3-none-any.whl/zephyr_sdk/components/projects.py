import requests
from zephyr_sdk.exceptions.ZExceptions import ZAPIError


# Get the details of all projects.
def get_all_normal_projects_details(client):
    url = client.base_url + '/project/details'
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Gets the id of all projects, and returns them in an array.
def get_all_normal_project(client):
    url = client.base_url + '/project/normal'
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Gets the id of every project lead.
def get_lead_for_all_projects(client):
    url = client.base_url + '/project/all/leads'
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Gets project details by the id passed in.
def get_project_by_id(client, project_id):
    url = client.base_url + '/project/' + str(project_id)
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Gets the team count for all projects
def get_project_team_count_for_all_projects(client):
    url = client.base_url + '/project/count/allprojects'
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Gets the number of projects each user is a member of.
def get_project_team_count_for_all_users(client):
    url = client.base_url + '/project/count/allusers'
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Get the user ids for the teams for all projects
def get_project_team_for_allocated_projects(client):
    url = client.base_url + '/project/allocated/projects'
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Get the user ids of the members on a specific project
def get_project_team_for_project(client, project_id):
    url = client.base_url + '/project/projectteam/' + str(project_id)
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Get all projects
def get_all_projects(client, include_inactive):
    url = client.base_url + '/project?includeinactive=' + str(include_inactive)
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()


# Light call to get all projects. Only ids and names
def get_all_projects_lite(client):
    url = client.base_url + '/project/lite'
    headers = {
        'Authorization': 'Bearer ' + client.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ZAPIError(r.status_code, r.json())

    return r.json()
