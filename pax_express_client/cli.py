from typing import Optional
import pathlib

import typer

import pax_express_client.client
import pax_express_client.api.packages.files

app = typer.Typer()

firmware = typer.Typer()

@firmware.command()
def upload(dist: Optional[pathlib.Path] = None):
    client = pax_express_client.client.Client()
    pax_express_client.api.packages.files.sync(user="", repo="", package="", version="")


@firmware.command()
def list(dist: Optional[pathlib.Path] = None):
    raise NotADirectoryError()

app.add_typer(firmware, name="fw")


@app.command()
def devices(dist: Optional[pathlib.Path] = None):
    typer.echo(f"Hello {dist}")


@app.command()
def login():
    email = typer.prompt("email")
    password = typer.prompt("password", hide_input=True)


@app.command()
def info():
    """show current context"""
    raise NotImplementedError()


@app.command()
def register():
    email = typer.prompt("email")
    username = typer.prompt("username")
    while True:
        password = typer.prompt("password", hide_input=True)
        password_repeat = typer.prompt("password (repeat)", hide_input=True)
        if password == password_repeat:
            break
        typer.echo("Password mismatch")


if __name__ == "__main__":
    app()
