from sqlalchemy.orm import Session
from repository.models import FolderMapping


class FolderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_share_name(self, share_name: str) -> FolderMapping | None:
        return (
            self.db.query(FolderMapping)
            .filter(FolderMapping.share_name == share_name)
            .first()
        )

    def create(self, share_name: str, disk_path: str) -> FolderMapping:
        mapping = FolderMapping(share_name=share_name, disk_path=disk_path)
        self.db.add(mapping)
        self.db.commit()
        self.db.refresh(mapping)
        return mapping

    def delete(self, share_name: str) -> None:
        mapping = self.get_by_share_name(share_name)
        if mapping:
            self.db.delete(mapping)
            self.db.commit()
