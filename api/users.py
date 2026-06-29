from fastapi import APIRouter, Depends
from dto.user_dto import UserCreateRequest, UserPasswordUpdateRequest
from application.user_service import UserService
from api.deps import get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
def create_user(req: UserCreateRequest, svc: UserService = Depends(get_user_service)):
    svc.create_user(req.username, req.password)
    return {"username": req.username, "created": True}


@router.delete("/{username}")
def delete_user(username: str, svc: UserService = Depends(get_user_service)):
    svc.delete_user(username)
    return {"username": username, "deleted": True}


@router.get("")
def list_users(svc: UserService = Depends(get_user_service)):
    return svc.list_users()


@router.put("/{username}/password")
def set_password(
    username: str, req: UserPasswordUpdateRequest, svc: UserService = Depends(get_user_service)
):
    svc.set_password(username, req.password)
    return {"username": username, "password_updated": True}
