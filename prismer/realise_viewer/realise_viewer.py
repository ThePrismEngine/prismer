import time
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List, Optional

from urllib3 import request

from prismer.realise_viewer.models import Realise, RealiseListAdapter
from prismer.utils.platform_utils import get_system_machine
from prismer.utils.request_decorator import request_decorator


class RealiseViewer(ABC):
    @abstractmethod
    def list(self) -> List[Realise]:
        pass

    @abstractmethod
    def by_tag(self, tag: str) -> Optional[Realise]:
        pass

class GithubRealiseViewer(RealiseViewer):
    root = "https://api.github.com"

    def __init__(self, repo: str) -> None:
        self.repo = repo
        self.releases_url = f"{self.root}/repos/{repo}/releases"
        self.releases_tags_url = f"{self.root}/repos/{repo}/releases/tags"
        self.download_url = f"https://github.com/{repo}/releases/download"

    @request_decorator
    @lru_cache(maxsize=None)
    def list(self) -> List[Realise]:
        request_data = request("GET", self.releases_url).json()
        return RealiseListAdapter.validate_python(request_data)

    @request_decorator
    def by_tag(self, tag: str) -> Optional[Realise]:
        request_data = request("GET", f"{self.releases_tags_url}/{tag}").json()
        return Realise.model_validate(request_data)

    def asset_url(self, tag: str):
        system, machine = get_system_machine()
        return f"{self. download_url}/{tag}/PrismEngine-{tag}-{system}-{machine}.zip"

github_realise_viewer = GithubRealiseViewer("ThePrismEngine/PrismEngine")