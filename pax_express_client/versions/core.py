from typing import Optional
import httpx
from .models import (
    VersionModel,
    VersionCreateBodyModel,
    VersionUpdateBodyModel,
    VersionGetFileVersionResponseModel,
)
from pax_express_client import get_url, response_handler


def get_latest(
    subject: str, repo: str, package: str, attribute_values: Optional[str] = None
):
    url = get_url(f"/packages/{subject}/{repo}/{package}/versions/_latest")
    params = {}
    if attribute_values:
        params.update({"attribute_values": attribute_values})
    response = httpx.get(url=url, params=params)
    return response_handler(response=response, return_model=VersionModel)


def get_version(
    subject: str, repo: str, package: str, version: str, attribute_values: int
):
    url = get_url(f"/packages/{subject}/{repo}/{package}/versions/{version}")
    params = {"attribute_values": attribute_values}
    response = httpx.get(url=url, params=params)
    return response_handler(response=response, return_model=VersionModel)


def create_version(body: VersionCreateBodyModel, subject: str, repo: str, package: str):
    url = get_url(f"/packages/{subject}/{repo}/{package}/versions")
    response = httpx.post(url=url, json=body.dict())
    response_handler(response=response, return_with_out_model=True)


def delete_version(subject: str, repo: str, package: str, version: str):
    url = get_url(f"/packages/{subject}/{repo}/{package}/versions/{version}")
    response = httpx.delete(url=url)
    return response_handler(response=response)


def update_version(
    body: VersionUpdateBodyModel, subject: str, repo: str, package: str, version: str
):
    url = get_url(f"/packages/{subject}/{repo}/{package}/versions/{version}")
    response = httpx.patch(url=url, json=body.dict())
    response_handler(response=response, return_with_out_model=True)


def get_version_for_file(subject: str, repo: str, file_path: str):
    url = get_url(f"/file_version/{subject}/{repo}/{file_path}")
    response = httpx.get(url=url)
    return response_handler(
        response=response, return_model=VersionGetFileVersionResponseModel
    )