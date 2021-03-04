from typing import Optional
import httpx
from .models import (
    RepoCreateBodyModel,
    RepoCreateResponseModel,
    RepoModel,
    ReposGetResponseModel,
    RepoUpdateBodyModel,
    RepoDeleteResponseModel,
    RepoSearchResponseModel,
)
from pax_express_client import get_url, response_handler
from ..authentication.core import get_auth_header_and_username


def create_repo(body: RepoCreateBodyModel) -> RepoCreateResponseModel:
    username, headers = get_auth_header_and_username()
    if username:
        url: str = get_url(f"/repos/{username}/{body.name}")
        response = httpx.post(url=url, json=body.dict(), headers=headers)
        return response_handler(response, RepoCreateResponseModel)


def get_repo(subject: str, repo: str) -> RepoModel:
    url: str = get_url(f"/repos/{subject}/{repo}")
    response = httpx.get(url=url)
    return response_handler(response, RepoModel)


def get_repos(subject: str) -> ReposGetResponseModel:
    url: str = get_url(f"/repos/{subject}")
    response = httpx.get(url=url)
    return response_handler(response=response, return_with_out_model=True)


def update_repo(body: RepoUpdateBodyModel, repo: str):
    username, headers = get_auth_header_and_username()
    if username:
        url: str = get_url(f"/repos/{username}/{repo}")
        response = httpx.patch(url=url, json=body.dict(), headers=headers)
        response_handler(response=response)


def delete_repo(repo: str) -> RepoDeleteResponseModel:
    username, headers = get_auth_header_and_username()
    if username:
        url: str = get_url(f"/repo/{username}/{repo}")
        response = httpx.delete(url=url, headers=headers)
        return response_handler(response, RepoDeleteResponseModel)


def search_repo(
    name: Optional[str], description: Optional[str]
) -> RepoSearchResponseModel:
    url: str = get_url(f"/search/repos")
    params = {"name": name, "desc": description}
    response = httpx.get(url=url, params=params)
    return response_handler(response=response, return_with_out_model=True)


def link_repo():
    # todo : https://git.r0k.de/gr/internal/paxexpress/paxexpress/-/issues/12
    raise NotImplementedError()


def unlink_repo():
    # todo : https://git.r0k.de/gr/internal/paxexpress/paxexpress/-/issues/12
    raise NotImplementedError()
