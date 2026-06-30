"""
이 모듈만이 윈도우 파일서버와 실제로 통신한다 (pywinrm 사용).
다른 계층(application/)은 이 클라이언트의 메서드만 호출하고,
PowerShell 문법을 직접 다루지 않는다 — WinRM 라이브러리를 나중에
바꾸거나 테스트용으로 모킹할 때 이 파일만 교체하면 되도록.

주의: 여기로 들어오는 모든 값(이름)은 호출 전에 core.validators로
이미 검증된 상태여야 한다 (방어선은 dto에서 한 번 더 걸지만,
이 계층에서도 검증되지 않은 원시 입력을 직접 받지 않는다).
"""
import json
import winrm
from config import WINRM_HOST, WINRM_USER, WINRM_PASSWORD, WINRM_TRANSPORT
from domain.permission import INHERITANCE_FLAGS, PROPAGATION_FLAGS


class WinRMError(RuntimeError):
    pass


class WinRMClient:
    def __init__(self):
        self._session = winrm.Session(
            WINRM_HOST,
            auth=(WINRM_USER, WINRM_PASSWORD),
            transport=WINRM_TRANSPORT,  # "ntlm" 또는 "basic" (basic이면 https 필수)
        )

    def _run_ps(self, script: str):
        result = self._session.run_ps(script)
        if result.status_code != 0:
            raise WinRMError(result.std_err.decode(errors="replace"))
        return result.std_out.decode(errors="replace")

    def _run_ps_json(self, script: str) -> list:
        """ConvertTo-Json 출력을 실제 Python list로 파싱해서 돌려준다.
        PowerShell의 ConvertTo-Json은 결과가 1건이면 배열이 아니라 단일
        객체를 내려주는 특성이 있어, 호출하는 쪽이 매번 그 경우를 신경
        쓰지 않도록 여기서 항상 list로 정규화한다."""
        raw = self._run_ps(script).strip()
        if not raw:
            return []
        data = json.loads(raw)
        return data if isinstance(data, list) else [data]

    # ---------- 사용자 ----------
    def create_user(self, username: str, password: str):
        script = (
            f'$pw = ConvertTo-SecureString "{password}" -AsPlainText -Force; '
            f'New-LocalUser -Name "{username}" -Password $pw -PasswordNeverExpires'
        )
        return self._run_ps(script)

    def delete_user(self, username: str):
        return self._run_ps(f'Remove-LocalUser -Name "{username}"')

    def list_users(self) -> list:
        # krbtgt(AD 시스템 계정), "이름$"로 끝나는 컴퓨터 계정은 우리가 만든
        # 업무용 계정이 아니므로 PowerShell 단계에서 미리 제외한다.
        script = (
            "Get-LocalUser "
            "| Where-Object { $_.Name -notlike '*$' -and $_.Name -ne 'krbtgt' } "
            "| Select-Object Name, Enabled "
            "| ConvertTo-Json"
        )
        return self._run_ps_json(script)

    def set_password(self, username: str, password: str):
        script = (
            f'$pw = ConvertTo-SecureString "{password}" -AsPlainText -Force; '
            f'Set-LocalUser -Name "{username}" -Password $pw'
        )
        return self._run_ps(script)

    # ---------- 그룹 ----------
    def create_group(self, group_name: str):
        return self._run_ps(f'New-LocalGroup -Name "{group_name}"')

    def delete_group(self, group_name: str):
        return self._run_ps(f'Remove-LocalGroup -Name "{group_name}"')

    def list_groups(self) -> list:
        return self._run_ps_json("Get-LocalGroup | Select-Object Name | ConvertTo-Json")

    def add_member(self, group_name: str, username: str):
        return self._run_ps(
            f'Add-LocalGroupMember -Group "{group_name}" -Member "{username}"'
        )

    def remove_member(self, group_name: str, username: str):
        return self._run_ps(
            f'Remove-LocalGroupMember -Group "{group_name}" -Member "{username}"'
        )

    def list_members(self, group_name: str) -> list:
        return self._run_ps_json(
            f'Get-LocalGroupMember -Group "{group_name}" | Select-Object Name | ConvertTo-Json'
        )

    # ---------- 폴더 + 공유 (Default Deny로 생성) ----------
    def create_folder_and_share(self, share_name: str, disk_path: str):
        script = f"""
New-Item -Path "{disk_path}" -ItemType Directory -Force | Out-Null

$acl = Get-Acl "{disk_path}"
$acl.SetAccessRuleProtection($true, $false)
foreach ($rule in @($acl.Access)) {{ $acl.RemoveAccessRule($rule) | Out-Null }}
$adminRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "BUILTIN\\Administrators", "FullControl", "{INHERITANCE_FLAGS}", "{PROPAGATION_FLAGS}", "Allow"
)
$systemRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "NT AUTHORITY\\SYSTEM", "FullControl", "{INHERITANCE_FLAGS}", "{PROPAGATION_FLAGS}", "Allow"
)
$acl.AddAccessRule($adminRule)
$acl.AddAccessRule($systemRule)
Set-Acl "{disk_path}" $acl

New-SmbShare -Name "{share_name}" -Path "{disk_path}" -FullAccess "Everyone" -FolderEnumerationMode AccessBased
"""
        return self._run_ps(script)

    def delete_folder_and_share(self, share_name: str, disk_path: str):
        script = f"""
Remove-SmbShare -Name "{share_name}" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "{disk_path}" -Recurse -Force -ErrorAction SilentlyContinue
"""
        return self._run_ps(script)

    # ---------- ACL ----------
    def grant_acl(self, disk_path: str, group: str, permissions: list[str], access_type: str):
        """
        permissions: FileSystemRights 이름 리스트 (예: ["ReadData", "WriteData"])
        access_type: "Allow" 또는 "Deny"

        PowerShell에서 여러 권한을 조합할 때는 쉼표로 이어 붙인 문자열
        ("ReadData,WriteData")을 FileSystemRights에 넘기면 자동 OR 합산됨.
        """
        rights_combined = ",".join(permissions)
        script = f"""
$acl = Get-Acl "{disk_path}"
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "{group}", "{rights_combined}", "{INHERITANCE_FLAGS}", "{PROPAGATION_FLAGS}", "{access_type}"
)
$acl.AddAccessRule($rule)
Set-Acl "{disk_path}" $acl
"""
        return self._run_ps(script)

    def revoke_acl(self, disk_path: str, group: str):
        script = f"""
$acl = Get-Acl "{disk_path}"
$acl.Access | Where-Object {{ $_.IdentityReference -like "*{group}" }} | ForEach-Object {{
    $acl.RemoveAccessRule($_) | Out-Null
}}
Set-Acl "{disk_path}" $acl
"""
        return self._run_ps(script)

    # ---------- 전체 공유 조회 ----------
    def list_shares(self) -> list:
        """
        C:\Shares 밑의 모든 하위 폴더를 한 번의 WinRM 호출로 훑어서
        공유 이름 + NTFS ACL 목록을 반환한다.
        Get-ChildItem + Get-Acl을 PowerShell 반복문 안에서 처리하므로
        WinRM 왕복은 항상 1번.
        Administrators / SYSTEM 같은 시스템 계정은 필터링해서 제외한다.
        """
        from config import WINDOWS_SHARE_BASE_PATH
        script = f"""
$result = @()
Get-ChildItem -Path "{WINDOWS_SHARE_BASE_PATH}" -Directory -ErrorAction SilentlyContinue | ForEach-Object {{
    $folder = $_
    $acl = Get-Acl $folder.FullName
    $acls = $acl.Access | Where-Object {{
        $_.IdentityReference -notlike "BUILTIN\\*" -and
        $_.IdentityReference -notlike "NT AUTHORITY\\*" -and
        $_.IdentityReference -ne "CREATOR OWNER"
    }} | ForEach-Object {{
        @{{
            Identity   = $_.IdentityReference.ToString()
            Rights     = $_.FileSystemRights.ToString()
            AccessType = $_.AccessControlType.ToString()
        }}
    }}
    $result += @{{
        ShareName = $folder.Name
        Path      = $folder.FullName
        Acls      = @($acls)
    }}
}}
$result | ConvertTo-Json -Depth 5
"""
        return self._run_ps_json(script)
