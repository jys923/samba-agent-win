import os

# WinRM 접속 정보 — 윈도우 파일서버
WINRM_HOST = os.environ.get("WINRM_HOST", "192.168.0.25")
WINRM_USER = os.environ.get("WINRM_USER", "Administrator")
WINRM_PASSWORD = os.environ.get("WINRM_PASSWORD", "")
WINRM_TRANSPORT = os.environ.get("WINRM_TRANSPORT", "ntlm")  # ntlm | basic(+https)

# 윈도우 쪽에 폴더를 만들 때 쓸 베이스 경로 (예: C:\Shares\Project1)
WINDOWS_SHARE_BASE_PATH = os.environ.get("WINDOWS_SHARE_BASE_PATH", r"C:\Shares")

# SQLite (share_name <-> 디스크경로 매핑 등)
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./winagent.db")
