from pydantic import BaseModel, field_validator
from core.validators import validate_name


class FolderCreateRequest(BaseModel):
    share_name: str

    @field_validator("share_name")
    @classmethod
    def _check(cls, v):
        return validate_name(v, "share_name")


class FolderResponse(BaseModel):
    share_name: str
    created: bool
