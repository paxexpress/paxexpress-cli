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
    DeviceProvisioningModel,
)
import httpx


def add_device():
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url("/devices/")
    body = pydantic_to_prompt(model=CreateDeviceModel)
    response = httpx.post(url=url, json=body.dict(), headers=header)
    response_handler(response=response, return_model=DeviceCreateResponseModel)


def update_device():
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url()


def get_device(mac_address: str):
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url(f"/devices/{mac_address}")
    response = httpx.get(url=url, headers=header)
    response_handler(response=response, return_model=DeviceModel, print_field="data")


def get_device_list():
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url("/devices/")
    response = httpx.get(url=url, headers=header)
    response = response_handler(response=response, print_field="data")


def delete_device(
    mac_address: str,
    is_operation_confirmed: bool = False,
):
    username, header = get_auth_header_and_username()
    if not username:
        return

    if not is_operation_confirmed and not is_operation_confirm():
        return
    url = get_url(f"/devices/{mac_address}")
    response = httpx.delete(url=url, headers=header)
    response_handler(response=response, return_model=DeviceDeleteResponseModel)


def get_device_provision_info(mac_address: str):
    username, header = get_auth_header_and_username()
    if not username:
        return
    url = get_url(f"/devices/{mac_address}/provision")
    response = httpx.get(url=url, headers=header)
    response_handler(
        response=response, return_model=DeviceProvisioningModel, print_field="data"
    )
