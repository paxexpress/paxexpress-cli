from typing import Optional
from .models import (
    PackageModel,
    PackageCreateBodyModel,
    PackageGetResponseModel,
    PackageDeleteResponseModel,
    PackageUpdateBodyModel,
)
from pax_express_client import get_url, response_handler
import httpx
from ..authentication.core import get_auth_header_and_username


def get_all_packages(
    subject: str, repo: str, start_pos: Optional[int], start_name: Optional[str]
):
    url = get_url(f"/repos/{subject}/{repo}/packages")
    params = {}
    if start_name:
        params.update({"start_name": start_name})
    if start_pos:
        params.update({"start_pos": start_pos})
    response = httpx.get(url=url, params=params)
    return response_handler(response=response, return_with_out_model=True)


def get_package(subject: str, package: str, repo: str, attribute_values: int):
    url = get_url(f"/packages/{subject}/{repo}/{package}")
    params = {"attribute_values": attribute_values}
    response = httpx.get(url=url, params=params)
    return response_handler(response=response, return_model=PackageModel)


def create_package(body: PackageCreateBodyModel, repo: str):
    username, headers = get_auth_header_and_username()
    if username:
        url = get_url(f"/packages/{username}/{repo}")
        response = httpx.post(url=url, json=body.dict(), headers=headers)
        return response_handler(response=response)


def delete_package(repo: str, package: str):
    username, headers = get_auth_header_and_username()
    if username:
        url = get_url(f"/packages/{username}/{repo}/{package}")
        response = httpx.delete(url=url, headers=headers)
        return response_handler(
            response=response, return_model=PackageDeleteResponseModel
        )


def update_package(body: PackageUpdateBodyModel, repo: str, package: str):
    username, headers = get_auth_header_and_username()
    if username:
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


def package_for_file(subject: str, repo: str, file_path: str):
    url = get_url(f"/file-package/{subject}/{repo}/{file_path}")
    response = httpx.get(url=url)
    return response_handler(response=response, return_model=PackageModel)
