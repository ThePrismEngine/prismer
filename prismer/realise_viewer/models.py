from datetime import datetime
from typing import List, Set

from pydantic import BaseModel, ConfigDict, TypeAdapter, Field, model_validator


class Realise(BaseModel):
    id: int
    tag_name: str
    name: str
    published_at: datetime
    md_body: str = Field(alias="body")
    supported_architectures: Set[str]
    supported_systems: Set[str]

    @model_validator(mode="before")
    @classmethod
    def calculate_supports(cls, data):
        if isinstance(data, dict):
            data = dict(data)

            targets_systs = set()
            targets_arch = set()
            for i in data["assets"]:
                splited_filename = i["name"][:-4].split("-")
                target_os, target_arch = splited_filename[2], splited_filename[3]
                targets_systs.add(target_os)
                targets_arch.add(target_arch)
            data["supported_architectures"] = list(targets_arch)
            data["supported_systems"] = list(targets_systs)

        return data

RealiseListAdapter = TypeAdapter(List[Realise])