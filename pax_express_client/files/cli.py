from typing import Optional
from typer import Typer, Option
from .core import (
    get_package_file,
    get_versions_file,
    files_search,
    file_upload,
    file_download,
)
from ..authentication.core import get_credential

file_cli = Typer(name="file")


@file_cli.command(name="versions-file", help="get version for file")
def versions_file(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    include_unpublished: bool = Option(
        False,
        "-ip",
        "--include_unpublished",
        help="include unpublished files",
    ),
):
    credential = get_credential()
    if credential:
        get_versions_file(
            subject=credential.user_name,
            repo=repo,
            package=package,
            include_unpublished=1 if include_unpublished else 0,
        )


@file_cli.command(name="packages-file", help="get package for file")
def packages_file(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    version: str = Option(..., "-v", "--version"),
    include_unpublished: bool = Option(
        False,
        "-ip",
        "--include_unpublished",
        help="include unpublished files",
    ),
):
    credential = get_credential()
    if credential:
        get_package_file(
            subject=credential.user_name,
            package=package,
            version=version,
            repo=repo,
            include_unpublished=1 if include_unpublished else 0,
        )


@file_cli.command(name="search", help="search for files")
def search(
    repo: str = Option(..., "-r", "--repo"),
    subject: str = Option(..., "-s", "--subject"),
    name: Optional[str] = Option(None, "-n", "--name"),
    sha1: Optional[str] = Option(None, "-sh", "--sha1"),
    start_pos: Optional[str] = Option(None, "-sp", "--start_pos"),
    create_after: Optional[str] = Option(None, "-ca", "--create_after"),
):
    files_search(
        name=name,
        subject=subject,
        repo=repo,
        start_pos=start_pos,
        create_after=create_after,
        sha1=sha1,
    )


@file_cli.command(name="upload", help="upload file")
def upload_file(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    version: str = Option(..., "-v", "--version"),
    filename: str = Option(..., "-fn", "--filename"),
):
    credential = get_credential()
    if credential:
        file_upload(
            subject=credential.user_name,
            repo=repo,
            package=package,
            version=version,
            filename=filename,
        )


@file_cli.command(name="download", help="download the file")
def download(
    repo: str = Option(..., "-r", "--repo"),
    filename: str = Option(..., "-fn", "--filename"),
    path_to_save: str = Option(..., "-ps", "--path_to_save"),
):
    credential = get_credential()
    if credential:
        file_download(
            subject=credential.user_name,
            repo=repo,
            file_name=filename,
            path_to_save=path_to_save,
        )
