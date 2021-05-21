from typing import Any, ClassVar, Dict, Optional, Callable, Union, List
from rich import print
import inquirer
import typer
from paxexpress_cli import env_settings
from httpx import Response
import keyring
import re
from rich.console import Console
from rich.table import Table
from rich.padding import Padding


names_regex = r"^([a-z]|[A-Z]|[0-9]|[-]|[.])+$"


def get_url(url: str) -> str:
    return f"{env_settings.API_ENDPOINT}{url}"


def print_status_table(
    result: Union[dict, list, str], is_success: bool, status_code: int
):
    table = Table(title="Request Status")
    table.add_column("State", style="green" if is_success else "red")
    table.add_column("Code", style="green" if is_success else "red")
    if isinstance(result, list):
        table.add_column("total")
        table.add_row(
            "Success" if is_success else "Failed",
            str(status_code),
            f"[red]{str(len(result))}",
        )
    else:
        table.add_row("Success" if is_success else "Failed", str(status_code))

    print(table)


def result_print(result: Union[dict, list, str], is_success: bool, status_code: int):
    print_status_table(result=result, is_success=is_success, status_code=status_code)
    if result is not None:
        if isinstance(result, list):
            print_list_as_table(result)
        elif isinstance(result, dict):
            print_dict_as_table(data=result)
        else:
            print(result)


def response_handler(
    response: Response,
    return_model: Optional[Callable] = None,
    return_with_out_model: Optional[bool] = False,
    print_result: bool = True,
):
    if response.status_code == 201 or response.status_code == 200:
        if print_result:
            result_print(
                response.json(), is_success=True, status_code=response.status_code
            )
        if return_model:
            return return_model(**response.json())
        elif return_with_out_model:
            return response.json()
    else:
        result_print(response.text, is_success=False, status_code=response.status_code)


def print_error(message: str):
    print(f"Error: [red bold] {message}")


def print_message(message: str):
    print(f"[green bold] {message}")


def print_dict_as_table(data: Dict):
    table = Table()
    table.add_column("Field Name", style="cyan")
    table.add_column("Field Value", style="green")
    for key in data.keys():
        table.add_row(key, str(data[key]))
    print(table)


def print_list_as_table(list_data: List[Dict]):
    table = Table()
    added_columns = []
    for data in list_data:
        for key in data.keys():
            if key not in added_columns:
                table.add_column(key, style="green")
                added_columns.append(key)
    for item in list_data:
        table.add_row(*[str(d) for d in list(item.values())])
    print(table)


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


def select_available_options(name: str, message: str, choices: list) -> Any:
    questions = [
        inquirer.List(
            name=name,
            message=message,
            choices=choices,
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers


def select_available_options_checkbox(
    name: str, message: str, choices: list
) -> List[Any]:
    questions = [
        inquirer.Checkbox(
            name=name,
            message=message,
            choices=choices,
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers
