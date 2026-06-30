from remote.client import WinRMClient
from application.folder_service import to_disk_path, FolderNotFoundError


class SharesService:
    def __init__(self, client: WinRMClient):
        self.client = client

    def list_shares(self) -> list:
        return self.client.list_shares()

    def get_share_detail(self, share_name: str) -> dict:
        disk_path = to_disk_path(share_name)
        if not self.client.folder_exists(disk_path):
            raise FolderNotFoundError(share_name)
        return self.client.get_share_detail(share_name, disk_path)
