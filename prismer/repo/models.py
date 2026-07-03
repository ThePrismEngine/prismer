from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class RealiseForList(BaseModel):
    id: int
    tag_name: str
    published_at: datetime

class RealiseForInstall(BaseModel):
    id: int
    tag_name: str
    name: str
    published_at: datetime

class ReleaseForShow(BaseModel):
    id: int
    tag_name: str
    name: str
    published_at: datetime
    body: str
    supported_architectures: List[str]
    supported_systems: List[str]