from pathlib import Path

import typer
from prismer.commands import engine, project
from prismer.utils import init

init()

app = typer.Typer(
    name="prismer",
    help="CLI для управления движком PrismEngine и проектами на нем",
)


app.add_typer(project.project_app, name="project")
app.add_typer(engine.engine_app, name="engine")

if __name__ == "__main__":
    app()
