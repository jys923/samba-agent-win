from fastapi import Depends
from remote.client import WinRMClient
from application.user_service import UserService
from application.group_service import GroupService
from application.folder_service import FolderService
from application.acl_service import AclService

# WinRM 세션은 호출마다 새로 만들지 않고 재사용 (연결 비용 절감)
_winrm_client = WinRMClient()


def get_winrm_client() -> WinRMClient:
    return _winrm_client


def get_user_service(client: WinRMClient = Depends(get_winrm_client)) -> UserService:
    return UserService(client)


def get_group_service(client: WinRMClient = Depends(get_winrm_client)) -> GroupService:
    return GroupService(client)


def get_folder_service(client: WinRMClient = Depends(get_winrm_client)) -> FolderService:
    return FolderService(client)


def get_acl_service(
    client: WinRMClient = Depends(get_winrm_client),
    folder_service: FolderService = Depends(get_folder_service),
) -> AclService:
    return AclService(client, folder_service)
