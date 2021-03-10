import os
from typing import Optional, Tuple
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
)
from pax_express_client import print_error, print_message, get_url, response_handler
import httpx
import keyring
import typer

pax_info_file_path = os.path.join(pathlib.Path.home(), ".pax_info")


def register(email: str, username: str, beta_key: str, password: str):
    url: str = get_url(url=f"/user/register")
    try:
        body = UserRegisterBodyModel(
            username=username,
            email=EmailStr(email),
            password=password,
            beta_key=beta_key,
        )
        response = httpx.post(url=url, json=body.dict())
        response_handler(response=response, return_model=UserRegisterResponseModel)
    except ValidationError:
        print_error("Check your inputs")


def login(email: str, password: str):
    url: str = get_url(f"/user/login")
    try:
        response = httpx.post(url=url, data={"username": email, "password": password})

        if response.status_code == 200:
            modeled_response = UserLoginResponseModel(**response.json())
            keyring.set_password(
                "pax.express", modeled_response.username, modeled_response.access_token
            )
            save_username(username=modeled_response.username)
            print_message(
                "You have successfully logged in \nYour login will expire after 30 Minutes"
            )
            return
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
