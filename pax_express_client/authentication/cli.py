import typer
from pax_express_client import print_error, custom_prompt
from . import core

authentication_cli = typer.Typer(name="authentication")


@authentication_cli.command(name="register", help="Register")
def register():
    email: str = typer.prompt("Email")
    username: str = custom_prompt(text="Username")
    beta_key: str = typer.prompt("Beta_Key")
    password = typer.prompt("Password", hide_input=True, confirmation_prompt=True)
    core.register(email=email, username=username, password=password, beta_key=beta_key)


@authentication_cli.command(name="login", help="Login")
def login():
    email: str = typer.prompt("Email")
    password = typer.prompt("Password", hide_input=True)
    core.login(email=email, password=password)


@authentication_cli.command(name="logout", help="Logout")
def logout():
    core.logout()


@authentication_cli.command(name="change-password", help="change the password")
def change_password():
    password = typer.prompt("Current password", hide_input=True)
    new_password: str = typer.prompt(
        "New password", hide_input=True, confirmation_prompt=True
    )
    core.change_password(current_password=password, new_password=new_password)
