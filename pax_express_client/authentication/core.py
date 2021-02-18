import os
from typing import Union
import yaml
from .models import Credential
from pax_express_client import print_error, print_message


# todo: https://git.r0k.de/gr/paxexpress-cli/-/issues/6
def login(user_name: str, password: str):
    save_credential(username=user_name, password=password)


def save_credential(username: str, password: str):
    with open(".credential", "w") as f:
        yaml.dump(
            {"user_name": username, "password": password}, f, default_flow_style=False
        )


def get_credential() -> Union[Credential, None]:
    try:
        with open(".credential", "r") as f:
            credential = yaml.safe_load(f)
            return Credential(**credential)
    except FileNotFoundError as ex:
        print_error("Please login!")


def remove_credential():
    try:
        os.remove(".credential")
    except FileNotFoundError:
        pass
    print_message("You have successfully logged out!")
