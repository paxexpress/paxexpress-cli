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


def create_repo(
    body: RepoCreateBodyModel, subject: str, repo: str
) -> RepoCreateResponseModel:
    url: str = get_url(f"/repos/{subject}/{repo}")
    response = httpx.post(url=url, json=body.dict())
    return response_handler(response, RepoCreateResponseModel)


def get_repo(subject: str, repo: str) -> RepoModel:
    url: str = get_url(f"/repos/{subject}/{repo}")
    response = httpx.get(url=url)
    return response_handler(response, RepoModel)


def get_repos(subject: str) -> ReposGetResponseModel:
    url: str = get_url(f"/repos/{subject}")
    response = httpx.get(url=url)
    return response_handler(response=response, return_with_out_model=True)


def update_repo(body: RepoUpdateBodyModel, subject: str, repo: str):
    url: str = get_url(f"/repos/{subject}/{repo}")
    response = httpx.patch(url=url, json=body.dict())
    response_handler(response=response)


def delete_repo(subject: str, repo: str) -> RepoDeleteResponseModel:
    url: str = get_url(f"/repo/{subject}/{repo}")
    response = httpx.delete(url=url)
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
