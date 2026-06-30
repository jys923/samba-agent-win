from pydantic import BaseModel, field_validator
from core.validators import validate_name, validate_permissions, validate_access_type


class AclGrantRequest(BaseModel):
    share_name: str
    group: str                     # 그룹명 또는 사용자명 (개인 폴더 케이스)
    permissions: list[str]         # FileSystemRights 이름 리스트 (비어있으면 검증 에러)
    access_type: str = "Allow"     # "Allow" 또는 "Deny"

    @field_validator("share_name")
    @classmethod
    def _check_share(cls, v):
        return validate_name(v, "share_name")

    @field_validator("group")
    @classmethod
    def _check_group(cls, v):
        return validate_name(v, "group")

    @field_validator("permissions")
    @classmethod
    def _check_permissions(cls, v):
        return validate_permissions(v)

    @field_validator("access_type")
    @classmethod
    def _check_access_type(cls, v):
        return validate_access_type(v)


class AclRevokeRequest(BaseModel):
    share_name: str
    group: str

    @field_validator("share_name")
    @classmethod
    def _check_share(cls, v):
        return validate_name(v, "share_name")

    @field_validator("group")
    @classmethod
    def _check_group(cls, v):
        return validate_name(v, "group")
