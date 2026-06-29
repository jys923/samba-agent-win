from fastapi import APIRouter, Depends
from dto.group_dto import GroupCreateRequest, GroupMemberRequest
from application.group_service import GroupService
from api.deps import get_group_service

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("")
def create_group(req: GroupCreateRequest, svc: GroupService = Depends(get_group_service)):
    svc.create_group(req.group_name)
    return {"group_name": req.group_name, "created": True}


@router.delete("/{group_name}")
def delete_group(group_name: str, svc: GroupService = Depends(get_group_service)):
    svc.delete_group(group_name)
    return {"group_name": group_name, "deleted": True}


@router.get("")
def list_groups(svc: GroupService = Depends(get_group_service)):
    return svc.list_groups()


@router.get("/{group_name}")
def get_group(group_name: str, svc: GroupService = Depends(get_group_service)):
    return {"group_name": group_name, "members": svc.list_members(group_name)}


@router.post("/{group_name}/members")
def add_member(
    group_name: str, req: GroupMemberRequest, svc: GroupService = Depends(get_group_service)
):
    svc.add_member(group_name, req.username)
    return {"group_name": group_name, "username": req.username, "added": True}


@router.delete("/{group_name}/members/{username}")
def remove_member(
    group_name: str, username: str, svc: GroupService = Depends(get_group_service)
):
    svc.remove_member(group_name, username)
    return {"group_name": group_name, "username": username, "removed": True}
