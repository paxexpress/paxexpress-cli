from typer import Typer, Option
from .core import *
from ..authentication.core import get_credential
from pax_express_client import pydantic_to_prompt

repo_cli = Typer(name="repository")


@repo_cli.command(name="all", help="get all repositories")
def get_all():
    credential = get_credential()
    if credential:
        get_repos(subject=credential.user_name)


@repo_cli.command(name="get", help="get a repository")
def get(repo: str = Option(..., "-r", "--repo")):
    credential = get_credential()
    if credential:
        get_repo(subject=credential.user_name, repo=repo)


@repo_cli.command(name="create", help="create a repository")
def create(repo: str = Option(..., "-r", "--repo")):
    credential = get_credential()
    if credential:
        body = pydantic_to_prompt(model=RepoCreateBodyModel)
        create_repo(body=body, subject=credential.user_name, repo=repo)


@repo_cli.command(name="update", help="update a repository")
def update(repo: str = Option(..., "-r", "--repo")):
    credential = get_credential()
    if credential:
        body = pydantic_to_prompt(model=RepoUpdateBodyModel)
        update_repo(body=body, repo=repo, subject=credential.user_name)


@repo_cli.command(name="delete", help="delete a repository")
def delete(repo: str = Option(..., "-r", "--repo")):
    credential = get_credential()
    if credential:
        delete_repo(subject=credential.user_name, repo=repo)


@repo_cli.command(name="search", help="search in repositories")
def search(
    name: Optional[str] = Option(None, "-n", "--name"),
    desc: Optional[str] = Option(None, "-d", "--desc"),
):
    credential = get_credential()
    if credential:
        search_repo(name=name, description=desc)
