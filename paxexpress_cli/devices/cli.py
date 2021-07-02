from paxexpress_cli.utils import custom_prompt, print_error
from typing import Optional
from typer import Typer, Option
from .core import (
    add_device,
    delete_device,
    get_device,
    get_device_list,
    get_device_provision_info,
    update_device,
)

device_cli = Typer(name="device", help="curd devices")


@device_cli.command(name="add", help="add new device")
def cli_add_device():
    add_device()


@device_cli.command(name="get", help="get device detail")
def cli_get_device():
    mac_address = custom_prompt(
        text="Device MAC address",
        regex="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
        regex_error_message="Invalid MAC address",
    )
    get_device(mac_address=mac_address)


@device_cli.command(name="list", help="get list of devices")
def cli_get_device_list():
    get_device_list()


@device_cli.command(name="delete", help="delete device")
def cli_delete_device(
    is_operation_confirmed: bool = Option(
        False,
        "-y",
        help="auto confirm operation",
    ),
):
    mac_address = custom_prompt(
        text="Device MAC address",
        regex="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
        regex_error_message="Invalid MAC address",
    )
    delete_device(
        mac_address=mac_address, is_operation_confirmed=is_operation_confirmed
    )


@device_cli.command(name="update", help="update device")
def cli_update_device(
    is_operation_confirmed: bool = Option(
        False,
        "-y",
        help="auto confirm operation",
    ),
):
    mac_address = custom_prompt(
        text="Device MAC address",
        regex="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
        regex_error_message="Invalid MAC address",
    )

    update_device(
        mac_address=mac_address,
        is_operation_confirmed=is_operation_confirmed,
    )
