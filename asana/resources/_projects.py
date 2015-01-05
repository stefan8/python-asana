# This file is automatically generated by generate.py using api.json

class _Projects:
    def __init__(self, client=None):
        self.client = client

    def create(self, params={}):
        return self.client.post('/projects', params)

    def update(self, project_id, params={}):
        path = '/projects/%d' % (project_id)
        return self.client.put(path, params)

    def find_by_id(self, project_id, params={}):
        path = '/projects/%d' % (project_id)
        return self.client.get(path, params)

    def find_by_workspace(self, workspace_id, params={}):
        path = '/workspaces/%d/projects' % (workspace_id)
        return self.client.get(path, params)

    def find_by_workspace_iterator(self, workspace_id, params={}):
        path = '/workspaces/%d/projects' % (workspace_id)
        return self.client.get_iterator(path, params)

    def find_all(self, params={}):
        return self.client.get('/projects', params)

    def find_all_iterator(self, params={}):
        return self.client.get_iterator('/projects', params)

    def create_in_workspace(self, workspace_id, params={}):
        path = '/workspaces/%d/projects' % (workspace_id)
        return self.client.post(path, params)

    def delete(self, project_id, params={}):
        path = '/projects/%d' % (project_id)
        return self.client.delete(path, params)
