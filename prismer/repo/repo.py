import platform
from typing import List

import urllib3

from prismer.repo.models import RealiseForList, RealiseForInstall, ReleaseForShow
from prismer.utils.platform_utils import get_system_machine

root = "https://api.github.com"
org = "ThePrismEngine"
repo_name = "PrismEngine"
repo = org + "/" + repo_name
releases_url = f"{root}/repos/{repo}/releases"
releases_tags_url = f"{root}/repos/{repo}/releases/tags/"
download_url = f"https://github.com/{repo}/releases/download"

def get_releases_for_list():
    r = urllib3.request("GET", releases_url)
    releases_for_list: List[RealiseForList] = []
    for i in r.json():
        releases_for_list.append(RealiseForList(**i))
    return releases_for_list


def get_release_for_install(tag_name: str):
    r = urllib3.request("GET", releases_tags_url+tag_name)
    return RealiseForInstall(**r.json())

def get_asset_path_for_this_version_and_platform(tag_name: str):
    system, machine = get_system_machine()
    return f"{download_url}/{tag_name}/PrismEngine-{tag_name}-{system}-{machine}.zip"

def get_release_for_show(tag_name: str):
    r = urllib3.request("GET", releases_tags_url+tag_name)
    data = r.json()
    targets_os = set()
    targets_arch = set()
    for i in data["assets"]:
        splited_filename = i["name"][:-4].split("-")
        target_os, target_arch = splited_filename[2], splited_filename[3]
        targets_os.add(target_os)
        targets_arch.add(target_arch)
    data["supported_architectures"] = list(targets_arch)
    data["supported_systems"] = list(targets_os)
    return ReleaseForShow(**data)