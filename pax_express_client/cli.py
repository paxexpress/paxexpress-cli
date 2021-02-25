from typer import Typer
from pax_express_client import repo_cli, authentication_cli, package_cli

cli = Typer()

cli.add_typer(repo_cli, name="repository", help="work with repositories")
cli.add_typer(authentication_cli, name="authentication", help="login and logout")
cli.add_typer(package_cli, name="package", help="Word with packages")

if __name__ == "__main__":
    cli()
