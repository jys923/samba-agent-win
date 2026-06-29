from fastapi import APIRouter, Depends
from dto.folder_dto import FolderCreateRequest
from application.folder_service import FolderService
from api.deps import get_folder_service

router = APIRouter(prefix="/folders", tags=["folders"])


@router.post("")
def create_folder(req: FolderCreateRequest, svc: FolderService = Depends(get_folder_service)):
    svc.create_folder(req.share_name)
    return {"share_name": req.share_name, "created": True}


@router.delete("/{share_name}")
def delete_folder(share_name: str, svc: FolderService = Depends(get_folder_service)):
    svc.delete_folder(share_name)
    return {"share_name": share_name, "deleted": True}
