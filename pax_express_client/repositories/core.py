from typing import Optional, Union
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
from pax_express_client import (
    get_url,
    response_handler,
    pydantic_to_prompt,
    is_operation_confirm,
    select_available_options,
    print_error,
)
from ..authentication.core import get_auth_header_and_username


def select_from_available_repo(subject: str) -> str:
    repos = get_repos(subject=subject, is_internal_call=True)
    if not repos:
        print_error("No repository has been created!")
        exit(1)
    repo = select_available_options(
        name="repo",
        choices=[item["name"] for item in repos],
        message="Select the repository",
    )
    if not repo:
        exit(1)
    return repo["repo"]


def create_repo():
    username, headers = get_auth_header_and_username()
    if not username:
        return
    body = pydantic_to_prompt(model=RepoCreateBodyModel)
    url: str = get_url(f"/repos/{username}/{body.name}")
    response = httpx.post(url=url, json=body.dict(), headers=headers)
    response_handler(response, RepoCreateResponseModel)


def get_repo(subject: str, repo: Optional[str]) -> RepoModel:
    if not repo:
        repo = select_from_available_repo(subject=subject)
    url: str = get_url(f"/repos/{subject}/{repo}")
    response = httpx.get(url=url)
    return response_handler(response, RepoModel)


def get_repos(subject: str, is_internal_call: bool = False) -> dict:
    url: str = get_url(f"/repos/{subject}")
    response = httpx.get(url=url)

    if not is_internal_call:
        response_handler(response=response, return_with_out_model=True)
        exit(0)
    return response.json()


def update_repo(repo: str, is_operation_confirmed: Optional[bool] = False):
    username, headers = get_auth_header_and_username()
    if not username:
        return
    body = pydantic_to_prompt(model=RepoUpdateBodyModel)
    if not is_operation_confirmed and not is_operation_confirm():
        return
    url: str = get_url(f"/repos/{username}/{repo}")
    response = httpx.patch(url=url, json=body.dict(), headers=headers)
    response_handler(response=response)


def delete_repo(repo: str, is_operation_confirmed: Optional[bool] = False):
    username, headers = get_auth_header_and_username()
    if not username:
        return
    if not is_operation_confirmed and not is_operation_confirm():
        return
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
