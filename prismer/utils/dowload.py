import zipfile
from pathlib import Path
from urllib.parse import urlparse

import typer
from rich.progress import Progress, SpinnerColumn, TransferSpeedColumn, DownloadColumn, TimeRemainingColumn
from urllib3 import PoolManager

from prismer.log.log import error
from prismer.repo.repo import get_asset_path_for_this_version_and_platform


def get_common_root_folder(members):
    if not members:
        return None

    root_components = set()
    for member in members:
        parts = member.filename.split('/')
        if parts and parts[0]:
            root_components.add(parts[0])

    if len(root_components) == 1:
        root = root_components.pop()
        has_content = any(m.filename.startswith(f"{root}/") and m.filename != f"{root}/" for m in members)
        if has_content:
            return root

    return None


def download_and_extract(url: str, output_path: Path):
    parsed_url = urlparse(url)
    filename = Path(parsed_url.path).name
    temp_filepath = Path(f"temp_{output_path.name}.zip")

    http = PoolManager()

    with Progress(SpinnerColumn(),
                  "[progress.description]{task.description}",
                  "[progress.percentage]{task.percentage:>3.0f}%",
                  DownloadColumn(),
                  TransferSpeedColumn(),
                  TimeRemainingColumn(),) as progress:
        with http.request("GET", url, preload_content=False, redirect=True) as response:
            if response.status == 404:
                error(f"Файла {url} не сушествует, возможно ваша архитектура или os пока не поддерживается")
            if response.status != 200:
                error(f"HTTP: {response.status}")

            total_size = int(response.headers.get('content-length', 0))

            task = progress.add_task(f"[cyan]Скачивание {filename}", total=total_size if total_size > 0 else None)

            chunk_size = 8192  # 8 KB
            with open(temp_filepath, "wb") as file:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)
                    progress.update(task, advance=len(chunk))

            response.release_conn()

    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(temp_filepath, 'r') as zip_ref:
            members = zip_ref.infolist()

            with Progress() as extract_progress:
                extract_task = extract_progress.add_task("[green]Распаковка", total=len(members))
                for member in members:
                        zip_ref.extract(member, output_dir)
                        extract_progress.update(extract_task, advance=1)
            old_dir = get_common_root_folder(members)
        (output_dir / old_dir).rename(output_path)

    except zipfile.BadZipFile:
        raise typer.Exit(code=1)

    finally:
        if temp_filepath.exists():
            temp_filepath.unlink()