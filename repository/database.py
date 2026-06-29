from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.models import Base
from config import DATABASE_URL

# SQLite는 기본적으로 동일 스레드만 같은 커넥션을 쓸 수 있는데,
# FastAPI는 요청마다 다른 스레드에서 처리할 수 있어 check_same_thread=False 필요.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
