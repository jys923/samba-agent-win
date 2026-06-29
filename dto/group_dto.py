from pydantic import BaseModel, field_validator
from core.validators import validate_name


class GroupCreateRequest(BaseModel):
    group_name: str

    @field_validator("group_name")
    @classmethod
    def _check(cls, v):
        return validate_name(v, "group_name")


class GroupMemberRequest(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def _check(cls, v):
        return validate_name(v, "username")


class GroupResponse(BaseModel):
    group_name: str
    members: list[str] = []
