from fastapi import APIRouter, Depends
from dto.acl_dto import AclGrantRequest, AclRevokeRequest
from application.acl_service import AclService
from api.deps import get_acl_service

router = APIRouter(prefix="/acl", tags=["acl"])


@router.post("")
def grant_acl(req: AclGrantRequest, svc: AclService = Depends(get_acl_service)):
    svc.grant(req.share_name, req.group, req.permission)
    return {
        "share_name": req.share_name,
        "group": req.group,
        "permission": req.permission,
        "granted": True,
    }


@router.delete("")
def revoke_acl(req: AclRevokeRequest, svc: AclService = Depends(get_acl_service)):
    svc.revoke(req.share_name, req.group)
    return {"share_name": req.share_name, "group": req.group, "revoked": True}
