import os
from typing import Optional, Tuple
from pydantic import EmailStr, ValidationError
import yaml
from .models import (
    UserRegisterBodyModel,
    UserRegisterResponseModel,
    UserLoginResponseModel,
)
from pax_express_client import print_error, print_message, get_url, response_handler
import httpx
import keyring
import typer


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


# todo: https://git.r0k.de/gr/paxexpress-cli/-/issues/6
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
            print_message("you have successfully logged in")
            return
        else:
            print_error(response.text)
            return
    except ValidationError:
        print_error("Check your inputs")


def logout():
    username = get_username()
    keyring.delete_password("pax.express", username)
    remove_info_file()
    print_message(f"You have successfully logged out {username}!")


def get_username() -> str:
    try:
        with open(".pax_info", "r") as f:
            info = yaml.safe_load(f)
            username = info.get("username", None)
            if username:
                return username
            else:
                print_error("Please login!")
    except FileNotFoundError as ex:
        username = typer.prompt("Username")
        save_username(username)
        return username


def save_username(username: str):
    with open(".pax_info", "w") as f:
        yaml.dump({"username": username}, f, default_flow_style=False)


def remove_info_file():
    try:
        os.remove(".pax_info")
    except FileNotFoundError:
        pass


def get_auth_header_and_username() -> Optional[Tuple[Optional[str], Optional[dict]]]:
    username = get_username()
    token: str = keyring.get_password("pax.express", username=username)
    if token:
        return username, {"Authorization": f"Bearer {token}"}
    print_error("Please login!")
    return None, None
