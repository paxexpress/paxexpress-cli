import os
from typing import Dict, List, Optional, Tuple
import pathlib

from keyring.errors import PasswordDeleteError
from pydantic import EmailStr, ValidationError
import yaml
from .models import (
    UserRegisterBodyModel,
    UserRegisterResponseModel,
    UserLoginResponseModel,
    UserUpdatePasswordBodyModel,
    UserUpdatePasswordResponseModel,
    ScopesGetValidResponseModel,
    AddUserScopesBodyModel,
    UserScopeAddResponseModel,
    DeleteScopeBodyModel,
    UserScopeDeleteResponseModel,
    UsersScopesGetResponseModel,
    GetLegalDocumentsResponseModel,
)
from paxexpress_cli import (
    print_error,
    print_message,
    get_url,
    response_handler,
    select_available_options_checkbox,
)
import httpx
import keyring
import typer
from paxexpress_cli import utils
import inquirer

pax_info_file_path = os.path.join(pathlib.Path.home(), ".pax_info")


def register(email: str, username: str, password: str):
    url: str = get_url(url=f"/user/register")
    try:
        body = UserRegisterBodyModel(
            username=username,
            email=EmailStr(email),
            password=password,
        )
        response = httpx.post(url=url, json=body.dict())
        response_handler(response=response, return_model=UserRegisterResponseModel)
    except ValidationError:
        print_error("Check your inputs")


def login(email: str, password: str, as_admin: bool = False):
    url: str = get_url(f"/user/login")
    try:
        data = {"username": email, "password": password}
        if as_admin:
            scopes = get_valid_scopes()
            if not scopes:
                print_error("No Scope has been selected!")
                exit(1)
            scopes = " ".join(scopes)
            data.update({"scope": scopes})
        response = httpx.post(url=url, data=data)

        if response.status_code == 200:
            modeled_response = UserLoginResponseModel(**response.json())
            keyring.set_password(
                "pax.express", modeled_response.username, modeled_response.access_token
            )
            save_username(username=modeled_response.username)
            print_message(
                "You have successfully logged in\nYour login will expire after [red bold]30[/] Minutes"
            )
            return
        elif response.status_code == 406:
            if response.json()["detail"].get("legal_documents"):
                show_available_legal_documents_list(
                    filter_by_legal_document_id=response.json()["detail"].get(
                        "legal_documents"
                    ),
                    username=response.json()["detail"].get("username"),
                    password=password,
                )

                login(email=email, password=password)

            pass
        else:
            print_error(response.text)
            return
    except ValidationError:
        print_error("Check your inputs")


def logout():
    username = get_username(is_logout=True)
    try:
        keyring.delete_password("pax.express", username)
    except PasswordDeleteError:
        pass
    remove_info_file()
    if username is not None:
        print_message(f"You have successfully logged out {username}!")


def get_username(is_logout: bool = False) -> Optional[str]:
    try:
        with open(pax_info_file_path, "r") as f:
            info = yaml.safe_load(f)
            username = info.get("username", None)
            if username:
                return username
            else:
                print_error("Please login!")
    except FileNotFoundError as ex:
        if not is_logout:
            username = typer.prompt("Username")
            # check if token exist for this username
            # if token exist, save username in .pax_info
            token: str = keyring.get_password("pax.express", username=username)
            if token:
                save_username(username)
                return username
            else:
                print_error("Please login!")
        else:
            print_error("Please login!")


def save_username(username: str):
    with open(pax_info_file_path, "w") as f:
        yaml.dump({"username": username}, f, default_flow_style=False)


def remove_info_file():
    try:
        os.remove(pax_info_file_path)
    except FileNotFoundError:
        pass


def get_auth_header_and_username() -> Optional[Tuple[Optional[str], Optional[dict]]]:
    username = get_username()
    token: str = keyring.get_password("pax.express", username=username)
    if token:
        return username, {"Authorization": f"Bearer {token}"}
    print_error("Please login!")
    return None, None


def change_password(current_password: str, new_password: str):
    username, headers = get_auth_header_and_username()
    if not username:
        return
    url = get_url(f"/user/profile/security/change-password")
    response = httpx.put(
        url=url,
        auth=httpx.BasicAuth(username=username, password=current_password),
        json=UserUpdatePasswordBodyModel(new_password=new_password).dict(),
    )
    response_handler(response=response, return_model=UserUpdatePasswordResponseModel)


def get_valid_scopes():
    url = get_url("/v1/authorization/scopes")
    response = httpx.get(url=url)
    result: ScopesGetValidResponseModel = response_handler(
        response=response, return_model=ScopesGetValidResponseModel, print_result=False
    )
    scopes = select_available_options_checkbox(
        name="Scopes", message="Select scopes", choices=result.valid_scopes
    )
    return scopes["Scopes"] if scopes else []


def add_scope(users_username: str):
    username, headers = get_auth_header_and_username()
    if not username:
        exit(1)
    scopes = get_valid_scopes()
    if not scopes:
        print_error("No Scope has been selected!")
        exit(1)
    url = get_url(f"/v1/authorization/user/{users_username}/scopes/add")
    body = AddUserScopesBodyModel(scopes=scopes)
    response = httpx.post(url=url, headers=headers, json=body.dict())
    response_handler(response=response, return_model=UserScopeAddResponseModel)


def remove_scope(users_username: str):
    username, headers = get_auth_header_and_username()
    if not username:
        exit(1)
    scopes = get_valid_scopes()
    if not scopes:
        print_error("No Scope has been selected!")
        exit(1)
    url = get_url(f"/v1/authorization/user/{users_username}/scopes")
    body = DeleteScopeBodyModel(scopes=scopes)
    response = httpx.patch(url=url, headers=headers, json=body.dict())
    response_handler(response=response, return_model=UserScopeDeleteResponseModel)


def get_users_scope(users_username: str):
    username, headers = get_auth_header_and_username()
    if not username:
        exit(1)
    url = get_url(f"/v1/authorization/user/{users_username}/scopes/get")
    response = httpx.get(url=url, headers=headers)
    response_handler(response=response, return_model=UsersScopesGetResponseModel)


def accept_legal_document(document_id: str, username: str, password: str):
    url = get_url(f"/v1/legals/{document_id}/accept")
    response = httpx.post(
        url=url, auth=httpx.BasicAuth(username=username, password=password)
    )
    response_handler(response=response, print_result=False)


def show_available_legal_documents_list(
    filter_by_legal_document_id: List[str], username: str, password: str
) -> GetLegalDocumentsResponseModel:
    url = get_url(f"/v1/legals")
    response = httpx.get(url=url)
    response: GetLegalDocumentsResponseModel = response_handler(
        print_result=False,
        response=response,
        return_model=GetLegalDocumentsResponseModel,
    )
    legal_documents_to_select = []
    for item in response.legal_documents:
        if item["id"] in filter_by_legal_document_id:
            legal_documents_to_select.append(item)

    count = len(legal_documents_to_select)
    print(f"There are {count} documents that must be accepted before you can proceed.")
    for document in legal_documents_to_select:
        document_id = document["id"]
        name = document["name"]
        url = get_url(document["url"])
        utils.print(f"Please carefully read our [bold]{name}[/bold].")
        utils.print("URL: " + url)
        questions = [
            inquirer.List(
                "open",
                message=f"Automatically open in browser?",
                choices=["Yes", "No"],
            ),
        ]
        result = inquirer.prompt(questions)
        if not result:
            exit(0)
        answer = result["open"]
        if answer == "Yes":
            import webbrowser

            webbrowser.open(url)
        questions = [
            inquirer.List(
                "accept",
                message=f"Do you accept?",
                choices=["Yes", "No"],
            ),
        ]
        result = inquirer.prompt(questions)
        if not result:
            exit(0)
        answer = result["accept"]
        if answer == "Yes":
            accept_legal_document(
                document_id=document_id,
                username=username,
                password=password,
            )
        else:
            utils.print(
                f"[bold red]Usage of pax.express is not possible without accepting {name}. Sorry."
            )
            exit(0)
