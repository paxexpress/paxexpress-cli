from typer import Typer
from pax_express_client import (
    repo_cli,
    authentication_cli,
    package_cli,
    file_cli,
    version_cli,
)

cli = Typer()

cli.add_typer(repo_cli, name="repository", help="work with repositories")
cli.add_typer(authentication_cli, name="authentication", help="login and logout")
cli.add_typer(package_cli, name="package", help="Work with packages")
cli.add_typer(version_cli, name="version", help="Work with versions")
cli.add_typer(file_cli, name="file", help="Work with files")

if __name__ == "__main__":
    cli()
