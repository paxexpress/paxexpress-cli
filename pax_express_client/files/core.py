from typing import Optional
import datetime
from pax_express_client import get_url, response_handler, print_message
import httpx
from pax_express_client import print_error
import os


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
    params = {"owner": subject, "repo": repo}
    if name and sha1:
        print_error("cant search name and sha1 at the same time")
        return
    if name:
        params.update({"name": {"$regex": f".*{name}.*"}})
    if sha1:
        params.update({"sha1": sha1})
    response = httpx.get(url=url, params=params)
    response_handler(response=response, return_with_out_model=True)


def file_upload(subject: str, repo: str, package: str, version: str, filename: str):
    url = get_url(f"/content/{subject}/{repo}/{package}/{version}/{filename}")

    with open(filename) as file:
        data = file.read()
        headers = {
            "x-bintray-publish": "1",
            "content-type": "application/octet-stream",
            "x-override-publish": "1",
        }
        response = httpx.put(url=url, data=data, headers=headers)
        response_handler(response=response, return_with_out_model=True)


def file_download(subject: str, repo: str, file_name: str, path_to_save: str):
    url = get_url(f"/{subject}/{repo}/storage/{file_name}")
    response = httpx.get(url=url)
    path = os.path.join(path_to_save, file_name)
    with open(path, "w") as file:
        file.write(response.text)
    print_message(f"file saved to {path}")
