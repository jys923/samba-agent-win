from fastapi import FastAPI
from fastapi.responses import JSONResponse
from repository.database import init_db
from core.validators import InvalidNameError
from remote.client import WinRMError
from application.folder_service import FolderNotFoundError
from api import users, groups, folders, acl

app = FastAPI(title="winagent", description="Windows 파일서버 원격 관리 에이전트")

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(folders.router)
app.include_router(acl.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.exception_handler(InvalidNameError)
def handle_invalid_name(request, exc: InvalidNameError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(FolderNotFoundError)
def handle_folder_not_found(request, exc: FolderNotFoundError):
    return JSONResponse(status_code=404, content={"detail": f"폴더(공유) 없음: {exc}"})


@app.exception_handler(WinRMError)
def handle_winrm_error(request, exc: WinRMError):
    return JSONResponse(status_code=502, content={"detail": f"WinRM 실행 실패: {exc}"})


@app.get("/health")
def health():
    return {"status": "ok"}
