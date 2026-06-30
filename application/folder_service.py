from remote.client import WinRMClient
from config import WINDOWS_SHARE_BASE_PATH


class FolderNotFoundError(LookupError):
    pass


class FolderAlreadyExistsError(ValueError):
    pass


def to_disk_path(share_name: str) -> str:
    """share_name으로부터 디스크 경로를 계산한다. DB에 저장하지 않고
    항상 이 규칙으로 계산 — WINDOWS_SHARE_BASE_PATH 밑 평평한 구조이므로
    share_name만 알면 경로가 항상 결정된다."""
    return f"{WINDOWS_SHARE_BASE_PATH}\\{share_name}"


class FolderService:
    def __init__(self, client: WinRMClient):
        self.client = client

    def create_folder(self, share_name: str) -> str:
        disk_path = to_disk_path(share_name)
        # 윈도우 파일시스템이 유일한 진실 — Test-Path로 직접 확인 후 생성.
        # 이미 있는 폴더에 또 만들면 ACL이 Administrators만으로 초기화되어
        # 기존 권한 설정이 날아갈 위험이 있으므로 반드시 생성 전에 확인.
        if self.client.folder_exists(disk_path):
            raise FolderAlreadyExistsError(share_name)
        self.client.create_folder_and_share(share_name, disk_path)
        return disk_path

    def delete_folder(self, share_name: str) -> None:
        disk_path = to_disk_path(share_name)
        if not self.client.folder_exists(disk_path):
            raise FolderNotFoundError(share_name)
        self.client.delete_folder_and_share(share_name, disk_path)

    def get_disk_path(self, share_name: str) -> str:
        disk_path = to_disk_path(share_name)
        if not self.client.folder_exists(disk_path):
            raise FolderNotFoundError(share_name)
        return disk_path
