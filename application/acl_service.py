from application.folder_service import FolderService


class AclService:
    def __init__(self, client, folder_service: FolderService):
        self.client = client
        self.folder_service = folder_service

    def grant(self, share_name: str, group: str, permissions: list[str], access_type: str):
        disk_path = self.folder_service.get_disk_path(share_name)
        self.client.grant_acl(disk_path, group, permissions, access_type)

    def revoke(self, share_name: str, group: str):
        disk_path = self.folder_service.get_disk_path(share_name)
        self.client.revoke_acl(disk_path, group)
