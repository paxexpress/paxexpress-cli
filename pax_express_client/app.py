from typer import Typer
from pax_express_client import repo_cli, authentication_cli

app = Typer()

app.add_typer(repo_cli, name="repository", help="work with repositories")
app.add_typer(authentication_cli, name="authentication", help="login and logout")

if __name__ == "__main__":
    app()
