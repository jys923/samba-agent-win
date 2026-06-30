from sqlalchemy.orm import Session
from remote.client import WinRMClient
from repository.folder_repo import FolderRepository
from application.folder_service import FolderNotFoundError


class SharesService:
    def __init__(self, client: WinRMClient, db: Session):
        self.client = client
        self.repo = FolderRepository(db)

    def list_shares(self) -> list:
        return self.client.list_shares()

    def get_share_detail(self, share_name: str) -> dict:
        mapping = self.repo.get_by_share_name(share_name)
        if mapping is None:
            raise FolderNotFoundError(share_name)
        return self.client.get_share_detail(share_name, mapping.disk_path)
