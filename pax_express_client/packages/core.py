from typing import Optional
from .models import (
    PackageModel,
    PackageCreateBodyModel,
    PackageDeleteResponseModel,
    PackageUpdateBodyModel,
)
from pax_express_client import (
    get_url,
    response_handler,
    pydantic_to_prompt,
    is_operation_confirm,
    print_error,
    select_available_options,
)
import httpx
from ..authentication.core import get_auth_header_and_username
from ..repositories import core as repositories_core


def select_from_available_packages(subject: str, repo: str):
    packages = get_all_packages(
        subject=subject,
        repo=repo,
        is_internal_call=True,
        start_pos=None,
        start_name=None,
    )
    if not packages:
        print_error("No packages has been created!")
        exit(1)
    package = select_available_options(
        name="package",
        choices=[package["name"] for package in packages],
        message="Select the package",
    )
    if not package:
        exit(1)
    return package["package"]


def get_all_packages(
    subject: str,
    repo: Optional[str],
    start_pos: Optional[int],
    start_name: Optional[str],
    is_internal_call: bool = False,
):
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=subject)
    url = get_url(f"/repos/{subject}/{repo}/packages")
    params = {}
    if start_name:
        params.update({"start_name": start_name})
    if start_pos:
        params.update({"start_pos": start_pos})
    response = httpx.get(url=url, params=params)
    if not is_internal_call:
        response_handler(response=response, return_with_out_model=True)
        exit(0)
    return response.json()


def get_package(
    subject: str, package: Optional[str], repo: Optional[str], attribute_values: int
):
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=subject)
    if not package:
        package = select_from_available_packages(subject=subject, repo=repo)

    url = get_url(f"/packages/{subject}/{repo}/{package}")
    params = {"attribute_values": attribute_values}
    response = httpx.get(url=url, params=params)
    return response_handler(response=response, return_model=PackageModel)


def create_package(repo: Optional[str]):
    username, headers = get_auth_header_and_username()
    if not username:
        return
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=username)
    body = pydantic_to_prompt(model=PackageCreateBodyModel)
    url = get_url(f"/packages/{username}/{repo}")
    response = httpx.post(url=url, json=body.dict(), headers=headers)
    return response_handler(response=response)


def delete_package(
    repo: Optional[str],
    package: Optional[str],
    is_operation_confirmed: Optional[bool] = False,
):
    username, headers = get_auth_header_and_username()
    if not username:
        exit(1)
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=username)
    if not package:
        package = select_from_available_packages(subject=username, repo=repo)
    if not is_operation_confirmed and not is_operation_confirm():
        exit(1)

    url = get_url(f"/packages/{username}/{repo}/{package}")
    response = httpx.delete(url=url, headers=headers)
    return response_handler(response=response, return_model=PackageDeleteResponseModel)


def update_package(
    repo: Optional[str],
    package: Optional[str],
    is_operation_confirmed: Optional[bool] = False,
):
    username, headers = get_auth_header_and_username()
    if not username:
        exit(1)
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=username)
    if not package:
        package = select_from_available_packages(subject=username, repo=repo)
    body = pydantic_to_prompt(PackageUpdateBodyModel)
    if not is_operation_confirmed and not is_operation_confirm():
        exit(1)

    url = get_url(f"/packages/{username}/{repo}/{package}")
    response = httpx.patch(url=url, json=body.dict(), headers=headers)
    response_handler(response=response)


def search_packages(
    name: Optional[str] = None,
    desc: Optional[str] = None,
    subject: Optional[str] = None,
    repo: Optional[str] = None,
):
    url = get_url("/search/packages")
    params = {}
    if name:
        params.update({"name": name})
    if subject:
        params.update({"subject": subject})
    if desc:
        params.update({"desc": desc})
    if repo:
        params.update({"repo": repo})
    response = httpx.get(url=url, params=params)
    return response_handler(response=response, return_with_out_model=True)


def maven_search():
    raise NotImplementedError()


def package_for_file(subject: str, repo: Optional[str], file_path: str):
    if not repo:
        repo = repositories_core.select_from_available_repo(subject=subject)
    url = get_url(f"/file-package/{subject}/{repo}/{file_path}")
    response = httpx.get(url=url)
    return response_handler(response=response, return_model=PackageModel)
