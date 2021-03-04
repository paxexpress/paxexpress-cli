from typer import Typer, Argument, Option, prompt
from .core import login as login_func, register as register_func, logout as logout_func
from pax_express_client import print_message, print_error

authentication_cli = Typer(name="authentication")


@authentication_cli.command(name="register", help="register")
def register():
    email: str = prompt("Email")
    username: str = prompt("Username")
    beta_key: str = prompt("Beta_Key")
    password: str = prompt("Password", hide_input=True)
    confirmed_password: str = prompt("Confirm password", hide_input=True)
    if password != confirmed_password:
        print_error("Please make sure your passwords match!")
    else:
        register_func(
            email=email, username=username, password=password, beta_key=beta_key
        )


@authentication_cli.command(name="login", help="login")
def login():
    email: str = prompt("Email")
    password = prompt("Password", hide_input=True)
    login_func(email=email, password=password)
    print_message("you have successfully logged in")


@authentication_cli.command(name="logout", help="logout")
def logout():
    logout_func()
