"""
윈도우 NTFS FileSystemRights 13개 세부 권한과 AccessControlType 정의.
이전의 4단계(read/write/full/deny) 단순화를 버리고, 윈도우가 실제로
쓰는 권한 이름 그대로 사용한다 — API 호출자가 윈도우 보안 탭과 동일한
멘탈모델로 권한을 지정할 수 있게 하기 위함.

permissions 리스트 + access_type 조합으로 PowerShell
FileSystemAccessRule을 직접 구성하므로, 여기 이름은 PowerShell의
[System.Security.AccessControl.FileSystemRights] 열거형 이름과 1:1 일치.
"""

# PowerShell FileSystemRights 허용 이름 (화이트리스트)
# 이 목록 외의 값은 core/validators.py에서 거부한다.
VALID_PERMISSIONS = frozenset({
    "ReadData",            # 파일 내용 읽기 / 폴더 목록 보기
    "WriteData",           # 파일 내용 덮어쓰기 / 폴더 안에 파일 생성
    "AppendData",          # 파일 끝에 추가 / 폴더 안에 하위 폴더 생성
    "ReadExtendedAttributes",   # 확장 특성 읽기
    "WriteExtendedAttributes",  # 확장 특성 쓰기
    "ExecuteFile",         # 실행파일 실행 / 폴더 탐색(트래버스)
    "DeleteSubdirectoriesAndFiles",  # 하위 폴더/파일 삭제
    "ReadAttributes",      # 기본 특성(숨김/읽기전용 등) 읽기
    "WriteAttributes",     # 기본 특성 쓰기
    "Delete",              # 해당 항목 자체 삭제
    "ReadPermissions",     # ACL 읽기
    "ChangePermissions",   # ACL 변경
    "TakeOwnership",       # 소유권 가져오기
})

# AccessControlType — Allow(허용) 또는 Deny(거부)
VALID_ACCESS_TYPES = frozenset({"Allow", "Deny"})

# 상속/전파 플래그 — 폴더 하위 전체에 적용하는 표준 설정
INHERITANCE_FLAGS = "ContainerInherit,ObjectInherit"
PROPAGATION_FLAGS = "None"
