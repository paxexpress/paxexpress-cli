from typing import Optional, Any
import datetime
from paxexpress_cli import (
    get_url,
    response_handler,
    print_message,
    get_auth_header_and_username,
    select_available_options,
)
from .models import FileDeleteResponseModel
import httpx
from paxexpress_cli import print_error
import os
import typer
from paxexpress_cli.packages import core as packages_core
from paxexpress_cli.repositories import core as repositories


def get_versions_file(
    subject: str,
    repo: Optional[str],
    package: Optional[str],
    include_unpublished: Optional[int] = None,
    is_internal_call: bool = False,
):
    if not repo:
        repo = repositories.select_from_available_repo(subject=subject)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=subject, repo=repo
        )
    url = get_url(f"/packages/{subject}/{repo}/{package}/files")
    params = {}
    params.update({"include_unpublished": include_unpublished})
    response = httpx.get(url=url, params=params)
    if not is_internal_call:
        response_handler(response=response, return_with_out_model=True)
    else:
        return response.json()


def get_package_file(
    subject: str,
    repo: Optional[str],
    package: Optional[str],
    version: Optional[str],
    include_unpublished: int,
    is_internal_call: bool = False,
):
    if not repo:
        repo = repositories.select_from_available_repo(subject=subject)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=subject, repo=repo
        )
    if not version:
        version = select_from_available_versions(
            subject=subject, repo=repo, package=package, filename=None
        )
    url = get_url(f"/packages/{subject}/{repo}/{package}/versions/{version}/files")
    params = {}
    params.update({"include_unpublished": include_unpublished})
    response = httpx.get(url=url, params=params)

    if is_internal_call and response.status_code != 200:
        return None

    if not is_internal_call:
        response_handler(response=response, return_with_out_model=True)
    else:
        return response.json()


def files_search(
    subject: str,
    repo: Optional[str],
    name: Optional[str] = None,
    sha1: Optional[str] = None,
    start_pos: Optional[str] = None,
    create_after: Optional[datetime.datetime] = None,
):
    if not repo:
        repo = repositories.select_from_available_repo(subject=subject)
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


def file_upload(
    repo: Optional[str], package: Optional[str], version: str, filename: str
):
    username, header = get_auth_header_and_username()
    if not username:
        return
    if not repo:
        repo = repositories.select_from_available_repo(subject=username)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=username, repo=repo
        )
    file_path: str = filename
    if os.path.isabs(file_path):
        filename = os.path.basename(file_path)

    url = get_url(f"/content/{username}/{repo}/{package}/{version}/{filename}")
    try:
        with open(file_path, "br") as file:
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
    repo: Optional[str],
    package: Optional[str],
    version: Optional[str],
    file_name: Optional[str],
    path_to_save: str,
):
    if not repo:
        repo = repositories.select_from_available_repo(subject=subject)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=subject, repo=repo
        )
    if not version:
        version = select_from_available_versions(
            subject=subject, repo=repo, package=package, filename=file_name
        )

    if not file_name:
        file_name = select_from_available_files(
            subject=subject, repo=repo, package=package, version=version
        )
    url = get_url(f"/{subject}/{repo}/{package}/{version}/{file_name}")
    response = httpx.get(url=url)
    if response.status_code == 200:
        path = os.path.join(path_to_save, file_name)
        with open(path, "bw") as file:
            file.write(response.content)
        print_message(f"file saved to {path}")
    else:
        print_error(response.text)


def select_from_available_versions(
    subject: str, repo: str, package: str, filename: Optional[str]
) -> Optional[str]:
    files = get_versions_file(
        subject=subject,
        package=package,
        repo=repo,
        include_unpublished=1,
        is_internal_call=True,
    )
    if not files:
        print_error("No versions have been created!")
        exit(1)
    selected_version = select_available_options(
        name="version",
        message="Select the version",
        choices=[item["version"] for item in files]
        if not filename
        else [item["version"] for item in files if item["name"] == filename],
    )
    if not selected_version:
        print_error("No version has been selected!")
        exit(1)
    return selected_version["version"]


def select_from_available_files(subject: str, repo: str, package: str, version: str):
    files = get_package_file(
        subject=subject,
        repo=repo,
        package=package,
        version=version,
        include_unpublished=1,
        is_internal_call=True,
    )
    if not files:
        print_error("No files have been uploaded!")
        exit(1)
    selected_file = select_available_options(
        name="file",
        message="Select the file",
        choices=[item["name"] for item in files if item["version"] == version],
    )
    if not selected_file:
        print_error("No file has been selected!")
        exit(1)
    return selected_file["file"]


def delete_file(
    repo: Optional[str],
    package: Optional[str],
    version: Optional[str],
    filename: Optional[str],
):
    username, header = get_auth_header_and_username()
    if not username:
        return
    if not repo:
        repo = repositories.select_from_available_repo(subject=username)
    if not package:
        package = packages_core.select_from_available_packages(
            subject=username, repo=repo
        )
    if not version:
        version = select_from_available_versions(
            subject=username, repo=repo, package=package, filename=filename
        )

    if not filename:
        filename = select_from_available_files(
            subject=username, repo=repo, package=package, version=version
        )
    print_message(f"Deleting file {filename} version {version}")
    url = get_url(f"/{username}/{repo}/{package}/{version}/{filename}")
    password = typer.prompt("Password", hide_input=True)
    response = httpx.delete(
        url=url, auth=httpx.BasicAuth(username=username, password=password)
    )
    response_handler(response=response, return_model=FileDeleteResponseModel)
    return
