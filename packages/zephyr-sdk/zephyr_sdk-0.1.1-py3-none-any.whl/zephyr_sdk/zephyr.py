from zephyr_sdk.components import defects
from zephyr_sdk.components import projects
from zephyr_sdk.components import releases
from zephyr_sdk.components import requirements
from zephyr_sdk.components import requirementtrees
from zephyr_sdk.components import testcases
from zephyr_sdk.components import testcasetrees
from zephyr_sdk.components import users
from zephyr_sdk.exceptions.ZExceptions import ResourceNotFoundError
from zephyr_sdk.exceptions.ZExceptions import InsufficientContextError
from zephyr_sdk.exceptions.ZExceptions import MethodNotImplementedError


class ZClient:
    # Constructor for the zephyr client.
    def __init__(self, token, url):
        self.token = token
        self.base_url = url

        # Set user id for the API calls
        self.user_id = self.get_current_logged_in_users()['id']

        # Properties that are undeclared for now
        self.project_id = None
        self.project_name = None
        self.release_id = None
        self.req_tree_id = None
        self.testcase_tree_id = None

    # Methods to add context to the client itself.
    def set_project(self, project_name):
        # Find the project with the name passed in
        response = self.get_all_projects_lite()
        for project in response:
            # Set the project id and exit function if found
            if project['name'] == project_name:
                self.project_id = project['id']
                self.project_name = project_name
                return

        # If the method got to this point, than raise an exception.
        raise ResourceNotFoundError("Project", project_name)

    def set_release(self, release_name):
        # First check to see if the project was set
        if self.project_id is None:
            raise InsufficientContextError("Project")

        # Now find the release with the name passed in
        response = self.get_releases_for_a_project(self.project_id)
        for release in response:
            # Set the release id and exit the function if found
            if release['name'] == release_name:
                self.release_id = release['id']
                return

        # If the method got to this point, raise an exception
        raise ResourceNotFoundError("Release", release_name)

    def set_requirement_tree(self, tree_name):
        # First check to see if the project was set
        if self.project_id is None:
            raise InsufficientContextError("Project")

        # Now find the requirement tree with the specified name.
        response = self.get_requirement_tree_with_ids(self.project_id, self.release_id)
        for tree in response:
            # Set the requirement tree id to be the proper tree if found.
            if tree['name'] == tree_name:
                self.req_tree_id = tree['id']
                return

        # Raise an exception that tree was not found.
        raise ResourceNotFoundError("Requirement tree", tree_name)

    def set_testcase_tree(self, tree_name):
        # First check to see if release id has been set.
        if self.release_id is None:
            raise InsufficientContextError("Release")

        # Now make the API call to get the testcase tree ids
        response = self.get_testcase_tree_by_release_id()
        for tree in response:
            if tree['name'] == tree_name:
                self.testcase_tree_id = tree['id']
                return

        raise ResourceNotFoundError("Testcase Tree", tree_name)

    # Defects methods
    def create_defect(self, defect_spec):
        if 'projectId' not in defect_spec and self.project_id is not None:
            defect_spec['projectId'] = self.project_id
        if 'product' not in defect_spec and self.project_name is not None:
            defect_spec['product'] = self.project_name
        return defects.create_defect(self, defect_spec)

    # Projects methods
    def get_all_normal_projects_details(self):
        return projects.get_all_normal_projects_details(self)

    def get_all_normal_project(self):
        return projects.get_all_normal_project(self)

    def get_lead_for_all_projects(self):
        return projects.get_lead_for_all_projects(self)

    def get_project_by_id(self, project_id=None):
        if project_id is None:
            return projects.get_project_by_id(self, self.project_id)
        else:
            return projects.get_project_by_id(self, project_id)

    def get_project_team_count_for_all_projects(self):
        return projects.get_project_team_count_for_all_projects(self)

    def get_project_team_count_for_all_users(self):
        return projects.get_project_team_count_for_all_users(self)

    def get_project_team_for_allocated_projects(self):
        return projects.get_project_team_for_allocated_projects(self)

    def get_project_team_for_project(self, project_id=None):
        raise MethodNotImplementedError("This method produces too much output.")
        if project_id is None:
            return projects.get_project_team_for_project(self, self.project_id)
        else:
            return projects.get_project_team_for_project(self, project_id)

    def get_all_projects(self, include_inactive):
        raise MethodNotImplementedError("Response always returns empty.")
        return projects.get_all_projects(self, include_inactive)

    def get_all_projects_lite(self):
        return projects.get_all_projects_lite(self)

    # Releases methods
    def create_release(self, release_spec):
        if 'projectId' not in release_spec and self.project_id is not None:
            release_spec['projectId'] = self.project_id
        return releases.create_release(self, release_spec)

    def delete_release(self, release_id):
        return releases.delete_release(self, release_id)

    def get_release_by_release_id(self, release_id=None):
        if release_id is None:
            return releases.get_release_by_release_id(self, self.release_id)
        else:
            return releases.get_release_by_release_id(self, release_id)

    def get_releases_for_a_project(self, project_id=None):
        if project_id is None:
            return releases.get_releases_for_a_project(self, self.project_id)
        else:
            return releases.get_releases_for_a_project(self, project_id)

    # Requirements methods
    def create_requirement(self, requirement_spec):
        if 'requirementTreeId' not in requirement_spec and self.req_tree_id is not None:
            requirement_spec['requirementTreeId'] = self.req_tree_id
        return requirements.create_requirement(self, requirement_spec)

    def delete_requirement(self, req_id):
        return requirements.delete_requirement(self, req_id)

    def get_requirements(self, req_tree_id=None):
        if req_tree_id is None:
            return requirements.get_requirements(self, self.req_tree_id)
        else:
            return requirements.get_requirements(self, req_tree_id)

    def update_requirement(self, req_id, requirement_spec):
        return requirements.update_requirement(self, req_id, requirement_spec)

    # RequirementTrees methods
    def create_requirement_tree(self, req_tree_spec):
        if 'projectId' not in req_tree_spec and self.project_id is not None:
            req_tree_spec['projectId'] = self.project_id
        if 'releaseIds' not in req_tree_spec and self.release_id is not None:
            req_tree_spec['releaseIds'] = [self.release_id]
        if 'parentId' not in req_tree_spec and self.req_tree_id is not None:
            req_tree_spec['parentId'] = self.req_tree_id

        return requirementtrees.create_requirement_tree(self, req_tree_spec)

    def get_all_requirement_trees(self):
        return requirementtrees.get_all_requirement_trees(self)

    def get_requirement_tree_with_ids(self, project_id=None, release_id=None):
        if project_id is None:
            project_id = self.project_id
        if release_id is None:
            release_id = self.release_id

        return requirementtrees.get_requirement_tree_with_ids(self, project_id, release_id)

    # Testcases methods
    def create_testcase(self, testcase_spec):
        if 'testcase' not in testcase_spec:
            testcase_spec['testcase'] = {}
        if 'releaseId' not in testcase_spec['testcase'] and self.release_id is not None:
            testcase_spec['testcase']['releaseId'] = self.release_id
        if 'tcrCatalogTreeId' not in testcase_spec and self.testcase_tree_id is not None:
            testcase_spec['tcrCatalogTreeId'] = self.testcase_tree_id

        return testcases.create_testcase(self, testcase_spec)

    def map_testcase_to_requirements(self, map_spec):
        return testcases.map_testcase_to_requirements(self, map_spec)

    # Testcase tree methods
    def get_testcase_tree_by_release_id(self, release_id=None):
        if release_id is None:
            release_id = self.release_id
        return testcasetrees.get_testcase_tree_by_release_id(self, release_id)

    # Users methods
    def get_current_logged_in_users(self):
        return users.get_current_logged_in_users(self)
