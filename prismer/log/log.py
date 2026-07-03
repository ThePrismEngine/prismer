import typer


def error(message: str):
    typer.secho("Error: " + message, err=True)
    raise typer.Exit(code=1)

def info(message: str):
    typer.secho(message)

def warning(message: str):
    typer.secho("Warning: " + message, err=True)