from pathlib import Path

import typer

project_app = typer.Typer(
    name="project",
    help="Операции с проектами",
)

@project_app.command("create")
def create(
    name: str = typer.Argument(..., help="Название проекта"),
    version: str = typer.Option(
        ...,
        "--version", "-v",
        help="Версия движка под который будет создан проект, в формате v<x>.<y>.<z>"
    ),
    path: Path = typer.Option(
        Path.cwd,
        "--path", "-p",
        help="Директория с проектом (по умолчанию - текущая)",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True
    )
):
    print(name)
    print(version)
    print(path)

@project_app.command("build")
def build(config: str = "debug"):
    pass