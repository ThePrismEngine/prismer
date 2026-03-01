import urllib3

from prismer.db.models import Version

root = "https://api.github.com"
org = "ThePrismEngine"
repo_name = "PrismEngine"
repo = org + "/" + repo_name
releases_url = f"{root}/repos/{repo}/releases"

def get_list():
    r = list()
    for release in urllib3.request("GET", releases_url).json():
        r.append(Version(tag=release["tag_name"], name=release["name"], type=f"ghr|{release["id"]}", published_at=release["published_at"], path=None, install_at=None))
    return r