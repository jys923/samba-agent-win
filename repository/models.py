from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FolderMapping(Base):
    """share_name(논리적 공유명) <-> 실제 디스크 경로 매핑.
    CUSTO는 share_name만 알면 되고, 디스크 경로는 여기(에이전트 내부)에만 존재.
    """
    __tablename__ = "folder_mappings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    share_name = Column(String(64), unique=True, nullable=False, index=True)
    disk_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
