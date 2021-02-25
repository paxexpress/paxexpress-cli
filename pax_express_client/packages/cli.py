from typer import Typer, Option
from .core import *
from ..authentication.core import get_credential
from pax_express_client import pydantic_to_prompt

package_cli = Typer(name="package")


@package_cli.command(help="Get all packages")
def get_all(
    repo: str = Option(..., "-r", "--repo"),
    start_pos: Optional[str] = Option(None, "-sp", "--start_pos"),
    start_name: Optional[str] = Option(None, "-sn", "--start_name"),
):
    credential = get_credential()
    if credential:
        get_all_packages(
            subject=credential.user_name,
            repo=repo,
            start_pos=start_pos,
            start_name=start_name,
        )


@package_cli.command(help="Get a package")
def get(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
    attribute_values: Optional[str] = Option(
        None, "-av", "--attribute_values", help="1 or 0"
    ),
):
    credential = get_credential()
    if credential:
        args = {"subject": credential.user_name, "repo": repo, "package": package}
        if attribute_values:
            args.update({"attribute_values": attribute_values})
        get_package(**args)


@package_cli.command(help="Create a package")
def create(repo: str = Option(..., "-r", "--repo")):
    credential = get_credential()
    if credential:
        body = pydantic_to_prompt(model=PackageCreateBodyModel)
        create_package(body=body, subject=credential.user_name, repo=repo)


@package_cli.command(help="Delete a package")
def delete(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
):
    credential = get_credential()
    if credential:
        delete_package(subject=credential.user_name, repo=repo, package=package)


@package_cli.command(help="Update a package")
def update(
    repo: str = Option(..., "-r", "--repo"),
    package: str = Option(..., "-p", "--package"),
):
    credential = get_credential()
    body = pydantic_to_prompt(PackageUpdateBodyModel)
    if credential:
        update_package(
            body=body, subject=credential.user_name, repo=repo, package=package
        )


@package_cli.command(help="Search a package")
def search(
    name: Optional[str] = Option(None, "-n", "--name"),
    desc: Optional[str] = Option(None, "-d", "--desc"),
    repo: Optional[str] = Option(None, "-r", "--repo"),
):
    credential = get_credential()
    if credential:
        search_packages(name=name, subject=credential.user_name, desc=desc, repo=repo)


@package_cli.command(name="package_for_file", help="Get a file's package")
def get_package_for_file(
    repo: str = Option(..., "-r", "--repo"),
    file_path: str = Option(..., "-f", "--file_path"),
):
    credential = get_credential()
    if credential:
        package_for_file(subject=credential.user_name, repo=repo, file_path=file_path)
