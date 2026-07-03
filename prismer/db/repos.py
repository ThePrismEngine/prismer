from typing import Optional, List

from sqlalchemy import delete
from sqlmodel import Session, select

from prismer.db.db import DatabaseManager
from prismer.db.models import EngineVersion, Project

class EngineVersionRepository:
    def __init__(self, session: Session=DatabaseManager.get_session()):
        self.session = session

    def get_all(self) -> List[EngineVersion]:
        return list(self.session.exec(select(EngineVersion)).all())

    def get_by_github_id(self, github_id: int) -> Optional[EngineVersion]:
        return self.session.exec(
            select(EngineVersion).where(EngineVersion.github_id == github_id)
        ).first()

    def get_by_tag(self, tag: str) -> Optional[EngineVersion]:
        return self.session.exec(
            select(EngineVersion).where(EngineVersion.tag == tag)
        ).first()

    def create(self, version: EngineVersion) -> EngineVersion:
        self.session.add(version)
        self.session.commit()
        self.session.refresh(version)
        return version

    def update(self, version: EngineVersion) -> EngineVersion:
        self.session.add(version)
        self.session.commit()
        self.session.refresh(version)
        return version

    def delete_by_tag(self, tag: str):
        self.session.exec(delete(EngineVersion).where(EngineVersion.tag == tag))
        self.session.commit()


class ProjectRepository:
    def __init__(self, session: Session=DatabaseManager.get_session()):
        self.session = session

    def get_all(self, with_engine: bool = True) -> List[Project]:
        stmt = select(Project)
        if with_engine:
            stmt = stmt.join(EngineVersion, isouter=True)
        return list(self.session.exec(stmt).all())

    def get_by_name(self, name: str) -> Optional[Project]:
        return self.session.exec(
            select(Project).where(Project.name == name)
        ).first()

    def create(self, project: Project) -> Project:
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete(self, project: Project):
        self.session.delete(project)
        self.session.commit()