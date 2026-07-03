import shutil

import typer
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

from prismer.db.models import EngineVersion
from prismer.db.repos import EngineVersionRepository
from prismer.log.log import error, info
from prismer.repo.repo import get_releases_for_list, get_release_for_install, \
    get_asset_path_for_this_version_and_platform, get_release_for_show
from prismer.utils.dirs import versions_dir
from prismer.utils.dowload import download_and_extract

engine_app = typer.Typer(
    name="engine",
    help="Управление движком и его версиями"
)

@engine_app.command("install")
def install(version: str = typer.Option("latest", help="Версия движка для установки, вы можете посмотреть на вывод prismer engine list чтобы узнать доступные"),
            #self_compilation: bool = typer.Option(False, help="Компилировать из исходного кода самостоятельно, без готовых файлов из релиза")
            ):
    if (release := get_release_for_install(version)) is None:
        error(f"Версия {version} отсутствует, посмотрите prismer engine list")

    engine_version_repository = EngineVersionRepository()
    if engine_version_repository.get_by_github_id(release.id) is not None:
        error("Версия уже установленна")

    install_dir = versions_dir / version
    asset_url = get_asset_path_for_this_version_and_platform(version)
    try:
        download_and_extract(asset_url, install_dir)
        engine_version_repository.create(EngineVersion(github_id=release.id, tag=release.tag_name, name=release.name, published_at=release.published_at, lib_path=str(install_dir)))
    except Exception as e:
        shutil.rmtree(install_dir)
        error(str(e))

@engine_app.command("uninstall")
def uninstall(version: str = typer.Option("latest")):
    engine_version_repository = EngineVersionRepository()
    if engine_version_repository.get_by_tag(version) is None:
        error("Версия не установленна")

    install_dir = versions_dir / version
    shutil.rmtree(install_dir)

    engine_version_repository = EngineVersionRepository()
    engine_version_repository.delete_by_tag(version)
    info(f"Версия {version} успешно деинсталированна")

@engine_app.command("list")
def list_version():
    table = Table()
    table.add_column("Версия")
    table.add_column("Дата публикации")
    table.add_column("Установлена")
    try:
        releases_for_list = get_releases_for_list()
    except Exception as e:
        error(str(e))
    engine_version_repository = EngineVersionRepository()
    for release in releases_for_list:
        is_installed = not engine_version_repository.get_by_github_id(release.id) is None
        table.add_row(release.tag_name, release.published_at.strftime("%d.%m.%Y"), str(is_installed))

    Console().print(table)

@engine_app.command("show")
def show_version(version: str = typer.Option("latest")):
    table = Table(show_header=False, show_lines=True)

    release = get_release_for_show(version)

    table.add_row("Name", release.name)
    table.add_row("Tag name", release.tag_name)
    table.add_row("Published at", release.published_at.strftime("%d.%m.%Y"))
    table.add_row("ghr id", str(release.id))
    table.add_row("Supported systems", ", ".join(release.supported_systems))
    table.add_row("Supported architectures", ", ".join(release.supported_architectures))
    console = Console()
    console.print(table)

    markdown = Markdown(markup=release.body)
    console.print(markdown)

@engine_app.command("installed")
def installed():
    engine_version_repository = EngineVersionRepository()
    table = Table()
    table.add_column("Версия")
    table.add_column("Дата публикации")
    table.add_column("Дата установки")
    table.add_column("Путь")

    installed_versions =  engine_version_repository.get_all()
    for version in installed_versions:
        table.add_row(version.tag, version.published_at.strftime("%d.%m.%Y"), version.installed_at.strftime("%d.%m.%Y"), version.lib_path)

    Console().print(table)