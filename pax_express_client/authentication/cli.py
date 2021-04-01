import typer
from pax_express_client import print_error, custom_prompt
from . import core

authentication_cli = typer.Typer(name="authentication")
admin_auth = typer.Typer(name="admin")
authentication_cli.add_typer(admin_auth, name="admin")


@authentication_cli.command(name="register", help="Register")
def register():
    email: str = typer.prompt("Email")
    username: str = custom_prompt(text="Username")
    beta_key: str = typer.prompt("Beta_Key")
    password = typer.prompt("Password", hide_input=True, confirmation_prompt=True)
    core.register(email=email, username=username, password=password, beta_key=beta_key)


@authentication_cli.command(name="login", help="Login")
def login(
    login_as_admin: bool = typer.Option(
        False, "-a", "--as-admin", help="login as admin"
    )
):
    email: str = typer.prompt("Email")
    password = typer.prompt("Password", hide_input=True)
    core.login(email=email, password=password, as_admin=login_as_admin)


@authentication_cli.command(name="logout", help="Logout")
def logout():
    core.logout()


@authentication_cli.command(name="change-password", help="Change the password")
def change_password():
    password = typer.prompt("Current password", hide_input=True)
    new_password: str = typer.prompt(
        "New password", hide_input=True, confirmation_prompt=True
    )
    core.change_password(current_password=password, new_password=new_password)


@admin_auth.command(name="add-scope", help="Add user scope")
def add_scope(
    username: str = typer.Option(..., "-u", "--username", help="username of client")
):
    core.add_scope(users_username=username)


@admin_auth.command(name="delete-scope", help="Delete scope from user")
def delete_scope(
    username: str = typer.Option(..., "-u", "--username", help="username of client")
):
    core.remove_scope(users_username=username)


@admin_auth.command(name="user-scope", help="Get users scopes")
def get_users_scopes(
    username: str = typer.Option(..., "-u", "--username", help="username of client")
):
    core.get_users_scope(users_username=username)
