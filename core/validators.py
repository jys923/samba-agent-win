"""
share_name / group_name / username 등 WinRM(PowerShell)으로 그대로 전달되는
모든 식별자는 여기를 거쳐야 함. 쉘 인젝션 문자(;, &, |, `, $() 등)가
섞여 들어오는 것을 막기 위해 화이트리스트(허용 문자만 통과) 방식으로 검증한다.
블랙리스트(특수문자 하나씩 막기) 방식은 빠뜨리는 문자가 항상 생기므로 사용하지 않음.
"""
import re

# 영문/숫자/언더스코어/하이픈만 허용, 1~64자
NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


class InvalidNameError(ValueError):
    pass


def validate_name(value: str, field: str = "name") -> str:
    if not isinstance(value, str) or not NAME_PATTERN.match(value):
        raise InvalidNameError(
            f"{field}는 영문/숫자/_/- 조합 1~64자만 허용됩니다: {value!r}"
        )
    return value


# permission 값도 화이트리스트로 제한 (read/write/full/deny 외엔 거부)
ALLOWED_PERMISSIONS = {"read", "write", "full", "deny"}


def validate_permission(value: str) -> str:
    if value not in ALLOWED_PERMISSIONS:
        raise InvalidNameError(
            f"permission은 {sorted(ALLOWED_PERMISSIONS)} 중 하나여야 합니다: {value!r}"
        )
    return value
