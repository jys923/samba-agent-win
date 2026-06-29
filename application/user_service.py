from remote.client import WinRMClient


class UserService:
    def __init__(self, client: WinRMClient):
        self.client = client

    def create_user(self, username: str, password: str):
        self.client.create_user(username, password)

    def delete_user(self, username: str):
        self.client.delete_user(username)

    def list_users(self):
        return self.client.list_users()

    def set_password(self, username: str, password: str):
        self.client.set_password(username, password)
