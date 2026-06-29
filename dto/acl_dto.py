from pydantic import BaseModel, field_validator
from core.validators import validate_name, validate_permission


class AclGrantRequest(BaseModel):
    share_name: str
    group: str
    permission: str  # read | write | full | deny

    @field_validator("share_name")
    @classmethod
    def _check_share(cls, v):
        return validate_name(v, "share_name")

    @field_validator("group")
    @classmethod
    def _check_group(cls, v):
        return validate_name(v, "group")

    @field_validator("permission")
    @classmethod
    def _check_permission(cls, v):
        return validate_permission(v)


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
