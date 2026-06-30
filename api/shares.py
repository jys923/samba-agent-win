from fastapi import APIRouter, Depends
from application.shares_service import SharesService
from remote.client import WinRMClient
from api.deps import get_winrm_client

router = APIRouter(prefix="/shares", tags=["shares"])


def get_shares_service(client: WinRMClient = Depends(get_winrm_client)) -> SharesService:
    return SharesService(client)


@router.get("")
def list_shares(svc: SharesService = Depends(get_shares_service)):
    """C:\\Shares 밑의 모든 공유 폴더 + NTFS ACL 목록을 실시간 조회.
    WinRM 왕복 1번으로 전체를 한꺼번에 가져온다."""
    return svc.list_shares()
