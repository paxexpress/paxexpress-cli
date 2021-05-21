from typing import Optional
import httpx
from .models import (
    VersionModel,
    VersionCreateBodyModel,
    VersionUpdateBodyModel,
    VersionGetFileVersionResponseModel,
)
from paxexpress_cli import (
    get_url,
    response_handler,
    pydantic_to_prompt,
    is_operation_confirm,
)
from ..authentication.core import get_auth_header_and_username
from paxexpress_cli.repositories import core as repositories_core
from paxexpress_cli.packages import core as packages_core
from paxexpress_cli.files import core as files_core


def get_latest(
    subject: str,
    repo: Optional[str],
    package: Optional[str],
    attribute_values: Optional[str] = None,
):
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=subject)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=subject, repo=repo
        )
    url = get_url(f"/packages/{subject}/{repo}/{package}/versions/_latest")
    params = {}
    if attribute_values:
        params.update({"attribute_values": attribute_values})
    response = httpx.get(url=url, params=params)
    return response_handler(response=response, return_model=VersionModel)


def get_version(
    subject: str,
    repo: Optional[str],
    package: Optional[str],
    version: Optional[str],
    attribute_values: int,
):
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=subject)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=subject, repo=repo
        )
    if not version:
        version = files_core.select_from_available_versions(
            subject=subject, repo=repo, package=package, filename=None
        )
    url = get_url(f"/packages/{subject}/{repo}/{package}/versions/{version}")
    params = {"attribute_values": attribute_values}
    response = httpx.get(url=url, params=params)
    return response_handler(response=response, return_model=VersionModel)


def create_version(repo: Optional[str], package: Optional[str]):
    username, headers = get_auth_header_and_username()
    if not username:
        return
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=username)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=username, repo=repo
        )
    body = pydantic_to_prompt(model=VersionCreateBodyModel)
    url = get_url(f"/packages/{username}/{repo}/{package}/versions")
    response = httpx.post(url=url, json=body.dict(), headers=headers)
    response_handler(response=response, return_with_out_model=True)


def delete_version(
    repo: Optional[str],
    package: Optional[str],
    version: Optional[str],
    is_operation_confirmed: Optional[bool] = False,
):
    username, headers = get_auth_header_and_username()
    if not username:
        return
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=username)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=username, repo=repo
        )
    if not version:
        version = files_core.select_from_available_versions(
            subject=username, repo=repo, package=package, filename=None
        )
    if not is_operation_confirmed and not is_operation_confirm():
        return
    url = get_url(f"/packages/{username}/{repo}/{package}/versions/{version}")
    response = httpx.delete(url=url, headers=headers)
    return response_handler(response=response)


def update_version(
    repo: Optional[str],
    package: Optional[str],
    version: Optional[str],
    is_operation_confirmed: Optional[bool] = False,
):
    username, headers = get_auth_header_and_username()
    if not username:
        return
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=username)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=username, repo=repo
        )
    if not version:
        version = files_core.select_from_available_versions(
            subject=username, repo=repo, package=package, filename=None
        )
    body = pydantic_to_prompt(model=VersionUpdateBodyModel)
    if not is_operation_confirmed and not is_operation_confirm():
        return
    url = get_url(f"/packages/{username}/{repo}/{package}/versions/{version}")
    response = httpx.patch(url=url, json=body.dict(), headers=headers)
    response_handler(response=response, return_with_out_model=True)


def get_version_for_file(subject: str, repo: Optional[str], file_path: str):
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=subject)
    url = get_url(f"/file_version/{subject}/{repo}/{file_path}")
    response = httpx.get(url=url)
    return response_handler(
        response=response, return_model=VersionGetFileVersionResponseModel
    )
