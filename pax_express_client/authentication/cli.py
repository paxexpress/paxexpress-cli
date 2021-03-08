from typer import Typer, prompt
from pax_express_client import print_error, custom_prompt
from . import core

authentication_cli = Typer(name="authentication")


@authentication_cli.command(name="register", help="register")
def register():
    email: str = prompt("Email")
    username: str = custom_prompt(text="Username")
    beta_key: str = prompt("Beta_Key")
    for _ in range(3):
        password: str = prompt("Password", hide_input=True)
        confirmed_password: str = prompt("Confirm password", hide_input=True)
        if password != confirmed_password:
            print_error("Please make sure your passwords match!")
        else:
            core.register(
                email=email, username=username, password=password, beta_key=beta_key
            )
            break


@authentication_cli.command(name="login", help="login")
def login():
    email: str = prompt("Email")
    password = prompt("Password", hide_input=True)
    core.login(email=email, password=password)


@authentication_cli.command(name="logout", help="logout")
def logout():
    core.logout()
