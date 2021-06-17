from typing import Optional
from typer import Typer, Option
from .core import (
    get_latest,
    get_version,
    create_version,
    delete_version,
    update_version,
    get_version_for_file,
    get_packages_available_versions,
)

version_cli = Typer(name="version")


@version_cli.command(name="latest", help="Get latest version")
def latest(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
    attribute_values: Optional[str] = Option(
        None, "-a", "--attribute-values", help="1 or 0"
    ),
):

    get_latest(
        subject=subject,
        repo=repo,
        package=package,
        attribute_values=attribute_values,
    )


@version_cli.command(name="get", help="Get a version")
def get(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
    version: str = Option(None, "-v", "--version"),
    attribute_values: bool = Option(
        False,
        "-a",
        "--attribute-values",
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


@version_cli.command(name="available", help="Get available version")
def get_available(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
):

    get_packages_available_versions(
        subject=subject,
        repo=repo,
        package=package,
    )


@version_cli.command(name="create", help="Create a version")
def create(
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
):

    create_version(repo=repo, package=package)


@version_cli.command(name="delete", help="Delete a version")
def delete(
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
    version: str = Option(None, "-v", "--version"),
    is_operation_confirmed: bool = Option(
        False,
        "-y",
        help="auto confirm operation",
    ),
):

    delete_version(
        repo=repo,
        package=package,
        version=version,
        is_operation_confirmed=is_operation_confirmed,
    )


@version_cli.command(name="update", help="Update a version")
def update(
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
    version: str = Option(None, "-v", "--version"),
    is_operation_confirmed: bool = Option(
        False,
        "-y",
        help="auto confirm operation",
    ),
):

    update_version(
        repo=repo,
        version=version,
        package=package,
        is_operation_confirmed=is_operation_confirmed,
    )


@version_cli.command(name="files_version", help="Get a version")
def get_versions_file(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(None, "-r", "--repo"),
    file_path: str = Option(..., "-f", "--file-path"),
):

    get_version_for_file(subject=subject, repo=repo, file_path=file_path)
