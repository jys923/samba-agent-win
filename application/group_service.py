from remote.client import WinRMClient


class GroupService:
    def __init__(self, client: WinRMClient):
        self.client = client

    def create_group(self, group_name: str):
        self.client.create_group(group_name)

    def delete_group(self, group_name: str):
        self.client.delete_group(group_name)

    def list_groups(self):
        return self.client.list_groups()

    def add_member(self, group_name: str, username: str):
        self.client.add_member(group_name, username)

    def remove_member(self, group_name: str, username: str):
        self.client.remove_member(group_name, username)

    def list_members(self, group_name: str):
        return self.client.list_members(group_name)
