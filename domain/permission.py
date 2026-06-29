"""
우리 API의 4단계 권한(read/write/full/deny)을 윈도우 NTFS
FileSystemRights 값으로 변환하는 규칙. 이 매핑이 바뀌면 ACL 동작이
바뀌므로 domain 계층에 둔다 (application/winrm 계층에서 임의로
문자열을 조립하지 않도록).
"""

PERMISSION_TO_NTFS_RIGHTS = {
    "read": "ReadAndExecute",
    "write": "Modify",
    "full": "FullControl",
    # deny는 별도 처리 (AccessControlType.Deny로 들어가며 권한값 자체는
    # FullControl을 막는 형태로 사용 — winrm/client.py 참고)
    "deny": "FullControl",
}

INHERITANCE_FLAGS = "ContainerInherit,ObjectInherit"
PROPAGATION_FLAGS = "None"


def to_ntfs_rights(permission: str) -> str:
    return PERMISSION_TO_NTFS_RIGHTS[permission]


def to_access_control_type(permission: str) -> str:
    return "Deny" if permission == "deny" else "Allow"
