import shutil

import typer
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

from prismer.db.models import EngineVersion
from prismer.db.repos import EngineVersionRepository
from prismer.locales import _
from prismer.log.log import error, info
from prismer.realise_viewer import Realise, github_realise_viewer
from prismer.utils.dirs import versions_dir
from prismer.utils.dowload import download_and_extract

engine_app = typer.Typer(
    name="engine",
    help=_("Управление движком и его версиями")
)

@engine_app.command("install")
def install(version: str = typer.Option("latest", help=_("Версия движка для установки, вы можете посмотреть на вывод prismer engine list чтобы узнать доступные")),
            #self_compilation: bool = typer.Option(False, help="Компилировать из исходного кода самостоятельно, без готовых файлов из релиза")
            ):
    if (release := github_realise_viewer.by_tag(version)) is None:
        error(_("Версия {version} отсутствует, посмотрите prismer engine list").format(version=version))

    engine_version_repository = EngineVersionRepository()
    if engine_version_repository.get_by_github_id(release.id) is not None:
        error(_("Версия уже установлена"))

    install_dir = versions_dir / version
    asset_url = github_realise_viewer.by_tag(version)
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
        error(_("Версия не установлена"))

    install_dir = versions_dir / version
    shutil.rmtree(install_dir)

    engine_version_repository = EngineVersionRepository()
    engine_version_repository.delete_by_tag(version)
    info(_("Версия {version} успешно деинсталлирована").format(version=version))

@engine_app.command("list")
def list_version():
    table = Table()
    table.add_column(_("Версия"))
    table.add_column(_("Дата публикации"))
    table.add_column(_("Установлена"))
    try:
        releases_for_list = github_realise_viewer.list()
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

    release = github_realise_viewer.by_tag(version)

    table.add_row(_("Имя"), release.name)
    table.add_row(_("Имя тега"), release.tag_name)
    table.add_row(_("Опубликовано в"), release.published_at.strftime("%d.%m.%Y"))
    table.add_row(_("ghr id"), str(release.id))
    table.add_row(_("Поддерживаемые системы"), ", ".join(release.supported_systems))
    table.add_row(_("Поддерживаемые архитектуры"), ", ".join(release.supported_architectures))
    console = Console()
    console.print(table)

    markdown = Markdown(markup=release.body)
    console.print(markdown)

@engine_app.command("installed")
def installed():
    engine_version_repository = EngineVersionRepository()
    table = Table()
    table.add_column(_("Версия"))
    table.add_column(_("Дата публикации"))
    table.add_column(_("Дата установки"))
    table.add_column(_("Путь"))

    installed_versions =  engine_version_repository.get_all()
    for version in installed_versions:
        table.add_row(version.tag, version.published_at.strftime("%d.%m.%Y"), version.installed_at.strftime("%d.%m.%Y"), version.lib_path)

    Console().print(table)