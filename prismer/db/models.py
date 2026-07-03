from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class EngineVersion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    github_id: int = Field(unique=True, index=True)
    tag: str = Field(index=True)
    name: str
    lib_path: str
    published_at: datetime
    installed_at: datetime = Field(default_factory=datetime.now)

    projects: List["Project"] = Relationship(back_populates="engine_version")


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    directory_path: str
    created_at: datetime = Field(default_factory=datetime.now)

    engine_version_id: Optional[int] = Field(
        default=None,
        foreign_key="engineversion.id",
        ondelete="SET NULL"
    )

    engine_version: Optional[EngineVersion] = Relationship(back_populates="projects")