from os import name
from . import core
from typer import Typer

info_cli = Typer()


@info_cli.command(name="readme")
def readme():
    core.show_readme()


@info_cli.command(name="releasing")
def releasing():
    core.show_releasing()
