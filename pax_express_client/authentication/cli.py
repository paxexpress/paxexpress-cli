from typer import Typer, Argument, Option, prompt
from .core import login as login_func, remove_credential
from pax_express_client import print_message

authentication_cli = Typer(name="authentication")


@authentication_cli.command(name="login", help="login")
def login():
    username = prompt("Username or Organization's name: ")
    password = prompt("Password: ", hide_input=True)
    login_func(user_name=username, password=password)
    print_message("you have successfully logged in")


@authentication_cli.command(name="logout", help="logout")
def logout():
    remove_credential()
