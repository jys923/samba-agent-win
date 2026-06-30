from remote.client import WinRMClient


class SharesService:
    def __init__(self, client: WinRMClient):
        self.client = client

    def list_shares(self) -> list:
        return self.client.list_shares()
