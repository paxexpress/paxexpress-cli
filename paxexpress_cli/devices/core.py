from paxexpress_cli.utils import is_operation_confirm
from typer import prompt
from paxexpress_cli import (
    get_url,
    response_handler,
    print_message,
    get_auth_header_and_username,
    select_available_options,
    pydantic_to_prompt,
)
from .models import (
    CreateDeviceModel,
    DeviceCreateResponseModel,
    DeviceDeleteResponseModel,
    DeviceListResponseModel,
    DeviceModel,
    UpdateDeviceModel,
    DeviceOutModel,
)
import httpx


def add_device() -> None:
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url("/devices/")
    body = pydantic_to_prompt(model=CreateDeviceModel)
    response = httpx.post(url=url, json=body.dict(), headers=header)
    response_handler(response=response, return_model=DeviceCreateResponseModel)


def update_device(mac_address: str, is_operation_confirmed: bool = False) -> None:
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url("/devices/{mac_address}")
    body = pydantic_to_prompt(model=UpdateDeviceModel)
    if not is_operation_confirmed and not is_operation_confirm():
        return
    response = httpx.patch(url=url, json=body.dict(), headers=header)
    response_handler(response=response, return_model=DeviceModel)


def get_device(mac_address: str) -> None:
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url(f"/devices/{mac_address}")
    response = httpx.get(url=url, headers=header)
    response_handler(response=response, return_model=DeviceOutModel, print_field="data")


def get_device_list() -> None:
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url("/devices/")
    response = httpx.get(url=url, headers=header)
    response = response_handler(response=response, print_field="data")


def delete_device(
    mac_address: str,
    is_operation_confirmed: bool = False,
) -> None:
    username, header = get_auth_header_and_username()
    if not username:
        return

    if not is_operation_confirmed and not is_operation_confirm():
        return
    url = get_url(f"/devices/{mac_address}")
    response = httpx.delete(url=url, headers=header)
    response_handler(response=response, return_model=DeviceDeleteResponseModel)
