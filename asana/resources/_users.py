# This file is automatically generated by generate.py using api.json

class _Users:
    def __init__(self, client=None):
        self.client = client

    def me(self, params={}):
        return self.client.get('/users/me', params)

    def find_by_workspace(self, workspace_id, params={}):
        path = '/workspaces/%d/users' % (workspace_id)
        return self.client.get(path, params)

    def find_by_workspace_iterator(self, workspace_id, params={}):
        path = '/workspaces/%d/users' % (workspace_id)
        return self.client.get_iterator(path, params)

    def find_all(self, params={}):
        return self.client.get('/users', params)

    def find_all_iterator(self, params={}):
        return self.client.get_iterator('/users', params)

    def find_by_id(self, user_id, params={}):
        path = '/users/%d' % (user_id)
        return self.client.get(path, params)
