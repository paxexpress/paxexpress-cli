from typing import Any, ClassVar, Optional, Callable, Union, List
from pprint import pprint
import typer
from pax_express_client import env_settings
from httpx import Response
import keyring
import re

names_regex = r"^([a-z]|[A-Z]|[0-9]|[-]|[.])+$"


def get_url(url: str) -> str:
    return f"{env_settings.API_ENDPOINT}{url}"


def result_print(result: Union[dict, list, str], is_success: bool, status_code: int):
    if is_success:
        result_state = typer.style(text="Success", fg=typer.colors.GREEN, bold=True)
        status_code = typer.style(
            text=f"{status_code}", fg=typer.colors.GREEN, bold=True
        )
    else:
        result_state = typer.style(text="Failed", fg=typer.colors.RED, bold=True)
        status_code = typer.style(text=f"{status_code}", fg=typer.colors.RED, bold=True)
    line = typer.style(f"{'-' * 20 + 'result' + '-' * 20}", fg=typer.colors.YELLOW)
    typer.echo(f"State: {result_state} with code: {status_code}")
    typer.echo(line)

    if isinstance(result, list):
        item_count = typer.style(text=f"{len(result)}", fg=typer.colors.RED, bold=True)
        typer.echo(f" total items: {item_count}")
        mini_line = typer.style(f"{'-' * 20}", fg=typer.colors.YELLOW)
        typer.echo(mini_line)
    if result is not None:
        pprint(result)
        typer.echo(line)


def response_handler(
    response: Response,
    return_model: Optional[Callable] = None,
    return_with_out_model: Optional[bool] = False,
):
    if response.status_code == 201 or response.status_code == 200:
        result_print(response.json(), is_success=True, status_code=response.status_code)
        if return_model:
            return return_model(**response.json())
        elif return_with_out_model:
            return response.json()
    else:
        result_print(response.text, is_success=False, status_code=response.status_code)


def print_error(message: str):
    error = typer.style(text=f"{message}", fg=typer.colors.RED, bold=True)
    typer.echo(f"Error: {error}", err=True)


def print_message(message: str):
    message = typer.style(text=message, fg=typer.colors.GREEN, bold=True)
    typer.echo(message)


def pydantic_to_prompt(model: ClassVar) -> Any:
    example = model.Config.schema_extra.get("example")
    fields = model.__fields__
    data: dict = {}
    for item in fields:
        field_info = fields[item]
        field_type = field_info.outer_type_
        if example:
            example_value = example.get(field_info.name)
        else:
            example_value = None

        prompt = (
            f"{field_info.name} - [{'Required' if field_info.required else 'Optional'}] "
            f" [{field_info.outer_type_}]"
        )
        args = {"text": prompt, "type": field_info.type_}
        if not field_info.required:
            if example_value:
                args.update({"default": example_value})
            else:
                args.update({"default": ""})
        if field_info.name == "name":
            value = custom_prompt(**args)
        else:
            value = typer.prompt(**args)

        if value == "" and not field_info.required:
            data.update({field_info.name: None})
        else:
            if field_type == List[str]:
                values = value.split(",")
                data.update({field_info.name: values})
            else:
                data.update({field_info.name: value})

    return model(**data)


def custom_prompt(**kwargs):
    value = typer.prompt(**kwargs)
    while not re.match(names_regex, value, re.I):
        print_error(
            f"All names should be in {names_regex} format (e.g My-Package). Please try again! "
        )
        value = typer.prompt(**kwargs)
    return value


def is_operation_confirm() -> bool:
    value: str = typer.prompt("Are you sure [Y/N]", show_choices=True)
    if value.lower() in ["y", "yes"]:
        return True
    else:
        print_error("Operation cancelled by user!")
        return False
