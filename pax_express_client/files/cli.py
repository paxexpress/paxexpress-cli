from typing import Optional
from typer import Typer, Option
from .core import (
    get_package_file,
    get_versions_file,
    files_search,
    file_upload,
    file_download,
    delete_file,
)


file_cli = Typer(name="file")


@file_cli.command(name="versions-file", help="Get version for file")
def versions_file(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
    include_unpublished: bool = Option(
        False,
        "-U",
        "--include-unpublished",
        help="include unpublished files",
    ),
):
    get_versions_file(
        subject=subject,
        repo=repo,
        package=package,
        include_unpublished=1 if include_unpublished else 0,
    )


@file_cli.command(name="packages-file", help="List all files in a given package")
def packages_file(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
    version: str = Option(None, "-v", "--version"),
    include_unpublished: bool = Option(
        False,
        "-U",
        "--include-unpublished",
        help="include unpublished files",
    ),
):
    get_package_file(
        subject=subject,
        package=package,
        version=version,
        repo=repo,
        include_unpublished=1 if include_unpublished else 0,
    )


@file_cli.command(name="search", help="Search for files")
def search(
    repo: str = Option(None, "-r", "--repo"),
    subject: str = Option(..., "-s", "--subject"),
    name: Optional[str] = Option(None, "-n", "--name"),
    sha1: Optional[str] = Option(None, "--sha1"),
    start_pos: Optional[str] = Option(None, "--start-pos"),
    create_after: Optional[str] = Option(None, "--create-after"),
):
    files_search(
        name=name,
        subject=subject,
        repo=repo,
        start_pos=start_pos,
        create_after=create_after,
        sha1=sha1,
    )


@file_cli.command(name="upload", help="Upload file")
def upload_file(
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
    version: str = Option(..., "-v", "--version"),
    filename: str = Option(..., "-f", "--filename"),
):
    file_upload(
        repo=repo,
        package=package,
        version=version,
        filename=filename,
    )


@file_cli.command(name="download", help="Download the file")
def download(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
    version: str = Option(None, "-v", "--version"),
    filename: str = Option(None, "-f", "--filename"),
    path_to_save: str = Option(..., "-o", "--output-path"),
):
    file_download(
        subject=subject,
        repo=repo,
        file_name=filename,
        path_to_save=path_to_save,
        version=version,
        package=package,
    )


@file_cli.command(name="delete", help="Delete a file")
def delete(
    repo: str = Option(None, "-r", "--repo"),
    package: str = Option(None, "-p", "--package"),
    version: Optional[str] = Option(None, "-v", "--version"),
    filename: Optional[str] = Option(None, "-f", "--filename"),
):
    delete_file(repo=repo, package=package, version=version, filename=filename)
