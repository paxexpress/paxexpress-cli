from typing import Optional
import datetime
from pax_express_client import (
    get_url,
    response_handler,
    print_message,
    get_auth_header_and_username,
)
from .models import FileDeleteResponseModel
import httpx
from pax_express_client import print_error
import os
import typer


def get_versions_file(
    subject: str, repo: str, package: str, include_unpublished: Optional[int] = None
):
    url = get_url(f"/packages/{subject}/{repo}/{package}/files")
    params = {}
    params.update({"include_unpublished": include_unpublished})
    response = httpx.get(url=url, params=params)
    response_handler(response=response, return_with_out_model=True)


def get_package_file(
    subject: str,
    repo: str,
    package: str,
    version: str,
    include_unpublished: int,
):
    url = get_url(f"/packages/{subject}/{repo}/{package}/versions/{version}/files")
    params = {}
    params.update({"include_unpublished": include_unpublished})
    response = httpx.get(url=url, params=params)
    response_handler(response=response, return_with_out_model=True)


def files_search(
    subject: str,
    repo: str,
    name: Optional[str] = None,
    sha1: Optional[str] = None,
    start_pos: Optional[str] = None,
    create_after: Optional[datetime.datetime] = None,
):
    url = get_url(f"/search/file")
    params = {"subject": subject, "repo": repo}
    if name and sha1:
        print_error("cant search name and sha1 at the same time")
        return
    if name:
        params.update({"name": name})
    if sha1:
        params.update({"sha1": sha1})
    response = httpx.get(url=url, params=params)
    response_handler(response=response, return_with_out_model=True)


def file_upload(repo: str, package: str, version: str, filename: str):
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url(f"/content/{username}/{repo}/{package}/{version}/{filename}")
    try:
        with open(filename, "br") as file:
            data = file.read()
            headers = {
                "x-bintray-publish": "1",
                "content-type": "application/octet-stream",
                "x-bintray-override": "1",
            }
            headers.update(header)
            password = typer.prompt("Password", hide_input=True)
            response = httpx.put(
                url=url,
                data=data,
                headers=headers,
                auth=httpx.BasicAuth(username=username, password=password),
            )
            response_handler(response=response, return_with_out_model=True)
    except Exception as e:
        print_error(f"{e.args[0]}")


def file_download(
    subject: str,
    repo: str,
    package: str,
    version: str,
    file_name: str,
    path_to_save: str,
):
    url = get_url(f"/{subject}/{repo}/{package}/{version}/{file_name}")
    response = httpx.get(url=url)
    if response.status_code == 200:
        path = os.path.join(path_to_save, file_name)
        with open(path, "bw") as file:
            file.write(response.content)
        print_message(f"file saved to {path}")
    else:
        print_error(response.text)


def delete_file(repo: str, package: str, version: str, filename: str):
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url(f"/{username}/{repo}/{package}/{version}/{filename}")
    password = typer.prompt("Password", hide_input=True)
    response = httpx.delete(
        url=url, auth=httpx.BasicAuth(username=username, password=password)
    )
    response_handler(response=response, return_model=FileDeleteResponseModel)
