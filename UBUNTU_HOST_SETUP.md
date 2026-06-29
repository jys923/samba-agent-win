# winagent 설치 (PVE LXC, venv, 도커 미사용)

## 1. LXC 안에서 venv 구성
```bash
apt update && apt install -y python3-venv python3-pip
mkdir -p /opt/winagent
cd /opt/winagent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. 환경변수 설정
`winagent.service`의 `Environment=` 줄에 실제 윈도우 파일서버 정보로 채울 것:
- `WINRM_HOST`: 윈도우 파일서버 IP
- `WINRM_USER` / `WINRM_PASSWORD`: WinRM 접속용 관리자 계정
- `WINDOWS_SHARE_BASE_PATH`: 폴더를 만들 베이스 경로 (예: `C:\Shares`)

## 3. 윈도우 측 WinRM 활성화 (사전 작업)
```powershell
Enable-PSRemoting -Force
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "<리눅스에이전트IP>" -Force
Restart-Service WinRM
```
(NTLM 기준. 운영 환경에서는 HTTPS+Basic 또는 인증서 기반으로 강화 검토)

## 4. systemd 등록 + 기동
```bash
cp winagent.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now winagent
systemctl status winagent
```

## 5. 동작 확인
```bash
curl http://127.0.0.1:8000/health
```

## 인증 관련 주의
이 에이전트는 **인증을 의도적으로 생략**했습니다 — 로컬에서만 실행되고
CUSTO가 로컬에서 접근하는 전제입니다. 외부 네트워크에 노출하지 말 것
(`--host 127.0.0.1`로 바인딩되어 있는 것도 이 때문).
