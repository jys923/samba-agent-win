from pydantic import BaseModel, field_validator
from core.validators import validate_name


class UserCreateRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def _check_username(cls, v):
        return validate_name(v, "username")


class UserPasswordUpdateRequest(BaseModel):
    password: str


class UserResponse(BaseModel):
    username: str
    full_name: str | None = None
    enabled: bool = True
