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

# from ..authentication.core import get_credential
from pax_express_client import pydantic_to_prompt

version_cli = Typer(name="version")


@version_cli.command(name="latest", help="get latest version")
def latest(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    attribute_values: Optional[str] = Option(
        None, "-av", "--attribute_values", help="1 or 0"
    ),
):

    get_latest(
        subject=subject,
        repo=repo,
        package=package,
        attribute_values=attribute_values,
    )


@version_cli.command(name="get", help="get a version")
def get(
    subject: str = Option(..., "-s", "--subject"),
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

    get_version(
        subject=subject,
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

    body = pydantic_to_prompt(model=VersionCreateBodyModel)
    create_version(body=body, repo=repo, package=package)


@version_cli.command(name="delete", help="delete a version")
def delete(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    version: str = Option(..., "-v", "--version"),
):

    delete_version(repo=repo, package=package, version=version)


@version_cli.command(name="update", help="update a version")
def update(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    version: str = Option(..., "-v", "--version"),
):

    body = pydantic_to_prompt(model=VersionUpdateBodyModel)
    update_version(
        body=body,
        repo=repo,
        version=version,
        package=package,
    )


@version_cli.command(name="files_version", help="get a version")
def get_versions_file(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(..., "-r", "--repo"),
    file_path: str = Option(..., "-f", "--file_path"),
):

    get_version_for_file(subject=subject, repo=repo, file_path=file_path)
