from typer import Typer, Option
from .core import *
from pax_express_client import pydantic_to_prompt

repo_cli = Typer(name="repository")


@repo_cli.command(name="all", help="Get all repositories")
def get_all(subject: str = Option(..., "-s", "--subject")):
    get_repos(subject=subject)


@repo_cli.command(name="get", help="Get a repository")
def get(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(..., "-r", "--repo"),
):
    get_repo(subject=subject, repo=repo)


@repo_cli.command(name="create", help="Create a repository")
def create():
    create_repo()


@repo_cli.command(name="update", help="Update a repository")
def update(
    repo: str = Option(..., "-r", "--repo"),
    is_operation_confirmed: bool = Option(
        False,
        "-y",
        help="auto confirm operation",
    ),
):
    update_repo(repo=repo, is_operation_confirmed=is_operation_confirmed)


@repo_cli.command(name="delete", help="Delete a repository")
def delete(
    repo: str = Option(..., "-r", "--repo"),
    is_operation_confirmed: bool = Option(
        False,
        "-y",
        help="auto confirm operation",
    ),
):
    delete_repo(repo=repo, is_operation_confirmed=is_operation_confirmed)


@repo_cli.command(name="search", help="Search in repositories")
def search(
    name: Optional[str] = Option(None, "-n", "--name"),
    desc: Optional[str] = Option(None, "-d", "--desc"),
):
    search_repo(name=name, description=desc)
