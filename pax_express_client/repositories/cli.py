from typer import Typer, Option
from .core import *
from pax_express_client import pydantic_to_prompt

repo_cli = Typer(name="repository")


@repo_cli.command(name="all", help="get all repositories")
def get_all(subject: str = Option(..., "-s", "--subject")):
    get_repos(subject=subject)


@repo_cli.command(name="get", help="get a repository")
def get(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(..., "-r", "--repo"),
):
    get_repo(subject=subject, repo=repo)


@repo_cli.command(name="create", help="create a repository")
def create():
    body = pydantic_to_prompt(model=RepoCreateBodyModel)
    create_repo(body=body)


@repo_cli.command(name="update", help="update a repository")
def update(repo: str = Option(..., "-r", "--repo")):
    body = pydantic_to_prompt(model=RepoUpdateBodyModel)
    update_repo(body=body, repo=repo)


@repo_cli.command(name="delete", help="delete a repository")
def delete(repo: str = Option(..., "-r", "--repo")):
    delete_repo(repo=repo)


@repo_cli.command(name="search", help="search in repositories")
def search(
    name: Optional[str] = Option(None, "-n", "--name"),
    desc: Optional[str] = Option(None, "-d", "--desc"),
):
    search_repo(name=name, description=desc)
