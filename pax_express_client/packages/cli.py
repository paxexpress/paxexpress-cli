from typer import Typer, Option
from .core import *

from pax_express_client import pydantic_to_prompt

package_cli = Typer(name="package")


@package_cli.command(help="Get all packages")
def get_all(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(..., "-r", "--repo"),
    start_pos: Optional[str] = Option(None, "--start-pos"),
    start_name: Optional[str] = Option(None, "--start-name"),
):
    get_all_packages(
        subject=subject,
        repo=repo,
        start_pos=start_pos,
        start_name=start_name,
    )


@package_cli.command(help="Get a package")
def get(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    attribute_values: bool = Option(
        False,
        "-av",
        "--attribute_values",
        help="include attribute_values",
    ),
):
    get_package(
        subject=subject,
        repo=repo,
        package=package,
        attribute_values=1 if attribute_values else 0,
    )


@package_cli.command(help="Create a package")
def create(repo: str = Option(..., "-r", "--repo")):
    body = pydantic_to_prompt(model=PackageCreateBodyModel)
    create_package(body=body, repo=repo)


@package_cli.command(help="Delete a package")
def delete(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
):
    delete_package(repo=repo, package=package)


@package_cli.command(help="Update a package")
def update(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
):
    body = pydantic_to_prompt(PackageUpdateBodyModel)
    update_package(body=body, repo=repo, package=package)


@package_cli.command(help="Search a package")
def search(
    subject: str = Option(..., "-s", "--subject"),
    name: Optional[str] = Option(None, "-n", "--name"),
    desc: Optional[str] = Option(None, "-d", "--desc"),
    repo: Optional[str] = Option(None, "-r", "--repo"),
):
    search_packages(name=name, subject=subject, desc=desc, repo=repo)


@package_cli.command(name="package_for_file", help="Get a file's package")
def get_package_for_file(
    subject: str = Option(..., "-s", "--subject"),
    repo: str = Option(..., "-r", "--repo"),
    file_path: str = Option(..., "-f", "--file-path"),
):
    package_for_file(subject=subject, repo=repo, file_path=file_path)
