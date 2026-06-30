from fastapi import APIRouter, Depends
from application.shares_service import SharesService
from remote.client import WinRMClient
from api.deps import get_winrm_client

router = APIRouter(prefix="/shares", tags=["shares"])


def get_shares_service(client: WinRMClient = Depends(get_winrm_client)) -> SharesService:
    return SharesService(client)


@router.get("")
def list_shares(svc: SharesService = Depends(get_shares_service)):
    """C:\\Shares 밑 1단계 공유 폴더 전체 + NTFS ACL 목록을 실시간 조회.
    WinRM 왕복 1번으로 전체를 한꺼번에 가져온다."""
    return svc.list_shares()


@router.get("/{share_name}")
def get_share_detail(share_name: str, svc: SharesService = Depends(get_shares_service)):
    """특정 공유 하나를 골라 그 안의 하위 폴더 구조(재귀)와 각 폴더의 ACL을 조회.
    윈도우에서 직접 만든 폴더든 API로 만든 폴더든 구분 없이 조회된다
    (C:\\Shares 밑에 실제로 존재하면 전부 대상)."""
    return svc.get_share_detail(share_name)
