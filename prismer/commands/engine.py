import typer

import prismer.db.version
import prismer.repo.version

engine_app = typer.Typer(
    name="engine",
    help="Управление движком и его версиями"
)

@engine_app.command("install")
def install(version: str = typer.Option("latest", help="Версия движка для установки"),
            self_compilation: bool = typer.Option(False, help="Компилировать из исходного кода самостоятельно, без готовых файлов из релиза")):
    pass

@engine_app.command("list")
def list_version(installed: bool = typer.Option(True, help="Показать только установленные версии"),
                 limit: int = typer.Option(100, help="Ограничить количество выводимых записей")):
    v_list = list()
    if installed:
        for installed_version in prismer.db.version.get_list():
            limit -= 1
            print(installed_version)
            if not limit: break
    else:
        tags = list()
        for i in prismer.db.version.get_list():
            tags.append(i.tag)

        for version in prismer.repo.version.get_list():
            limit -= 1
            if version.tag in tags:
                print(str(version) + " - Installed")
            else:
                print(str(version) + " - Available")
            if not limit: break