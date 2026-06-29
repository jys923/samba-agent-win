from sqlalchemy.orm import Session
from remote.client import WinRMClient
from repository.folder_repo import FolderRepository
from config import WINDOWS_SHARE_BASE_PATH


class FolderNotFoundError(LookupError):
    pass


class FolderAlreadyExistsError(ValueError):
    pass


class FolderService:
    def __init__(self, client: WinRMClient, db: Session):
        self.client = client
        self.repo = FolderRepository(db)

    def create_folder(self, share_name: str) -> str:
        # WinRM 호출(윈도우 쪽 실제 폴더/공유 생성, ACL 초기화)보다 먼저 검사해야 함 —
        # 순서를 바꾸면 이미 있는 폴더의 권한 설정이 의도치 않게 초기화될 위험이 있음.
        if self.repo.get_by_share_name(share_name) is not None:
            raise FolderAlreadyExistsError(share_name)

        disk_path = f"{WINDOWS_SHARE_BASE_PATH}\\{share_name}"
        self.client.create_folder_and_share(share_name, disk_path)
        self.repo.create(share_name, disk_path)
        return disk_path

    def delete_folder(self, share_name: str) -> None:
        mapping = self.repo.get_by_share_name(share_name)
        if mapping is None:
            raise FolderNotFoundError(share_name)
        self.client.delete_folder_and_share(share_name, mapping.disk_path)
        self.repo.delete(share_name)

    def get_disk_path(self, share_name: str) -> str:
        mapping = self.repo.get_by_share_name(share_name)
        if mapping is None:
            raise FolderNotFoundError(share_name)
        return mapping.disk_path
