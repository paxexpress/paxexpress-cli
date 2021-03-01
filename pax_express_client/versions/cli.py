from typing import Optional
from typer import Typer, Option
from .core import (
    get_latest,
    get_version,
    create_version,
    delete_version,
    update_version,
    get_version_for_file,
)
from .models import VersionCreateBodyModel, VersionUpdateBodyModel
from ..authentication.core import get_credential
from pax_express_client import pydantic_to_prompt

version_cli = Typer(name="version")


@version_cli.command(name="latest", help="get latest version")
def latest(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    attribute_values: Optional[str] = Option(
        None, "-av", "--attribute_values", help="1 or 0"
    ),
):
    credential = get_credential()
    if credential:
        get_latest(
            subject=credential.user_name,
            repo=repo,
            package=package,
            attribute_values=attribute_values,
        )


@version_cli.command(name="get", help="get a version")
def get(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    version: str = Option(..., "-v", "--version"),
    attribute_values: bool = Option(
        False,
        "-av",
        "--attribute_values",
        help="include attribute_values",
    ),
):
    credential = get_credential()
    if credential:
        get_version(
            subject=credential.user_name,
            repo=repo,
            package=package,
            version=version,
            attribute_values=1 if attribute_values else 0,
        )


@version_cli.command(name="create", help="create a version")
def create(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
):
    credential = get_credential()
    if credential:
        body = pydantic_to_prompt(model=VersionCreateBodyModel)
        create_version(
            body=body, subject=credential.user_name, repo=repo, package=package
        )


@version_cli.command(name="delete", help="delete a version")
def delete(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    version: str = Option(..., "-v", "--version"),
):
    credential = get_credential()
    if credential:
        delete_version(
            subject=credential.user_name, repo=repo, package=package, version=version
        )


@version_cli.command(name="update", help="update a version")
def update(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    version: str = Option(..., "-v", "--version"),
):
    credential = get_credential()
    if credential:
        body = pydantic_to_prompt(model=VersionUpdateBodyModel)
        update_version(
            body=body,
            subject=credential.user_name,
            repo=repo,
            version=version,
            package=package,
        )


@version_cli.command(name="files_version", help="get a version")
def get_versions_file(
    repo: str = Option(..., "-r", "--repo"),
    file_path: str = Option(..., "-f", "--file_path"),
):
    credential = get_credential()
    if credential:
        get_version_for_file(
            subject=credential.user_name, repo=repo, file_path=file_path
        )
