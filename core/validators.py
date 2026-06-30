"""
WinRM(PowerShell)으로 그대로 전달되는 모든 식별자와 권한값은
여기서 화이트리스트 방식으로 검증한다.
블랙리스트(특수문자를 하나씩 막기)는 빠뜨리는 문자가 생기므로 사용 안 함.
"""
import re
from domain.permission import VALID_PERMISSIONS, VALID_ACCESS_TYPES

# 영문/숫자/언더스코어/하이픈만 허용, 1~64자
NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


class InvalidNameError(ValueError):
    pass


class InvalidPermissionError(ValueError):
    pass


def validate_name(value: str, field: str = "name") -> str:
    if not isinstance(value, str) or not NAME_PATTERN.match(value):
        raise InvalidNameError(
            f"{field}는 영문/숫자/_/- 조합 1~64자만 허용됩니다: {value!r}"
        )
    return value


def validate_permissions(permissions: list[str]) -> list[str]:
    """permissions 리스트가 비어있지 않은지, 모두 유효한 FileSystemRights 이름인지 검증."""
    if not permissions:
        raise InvalidPermissionError(
            "permissions는 비어있을 수 없습니다. "
            f"허용 값: {sorted(VALID_PERMISSIONS)}"
        )
    invalid = [p for p in permissions if p not in VALID_PERMISSIONS]
    if invalid:
        raise InvalidPermissionError(
            f"유효하지 않은 permission 값: {invalid}. "
            f"허용 값: {sorted(VALID_PERMISSIONS)}"
        )
    return permissions


def validate_access_type(value: str) -> str:
    if value not in VALID_ACCESS_TYPES:
        raise InvalidPermissionError(
            f"access_type은 {sorted(VALID_ACCESS_TYPES)} 중 하나여야 합니다: {value!r}"
        )
    return value
