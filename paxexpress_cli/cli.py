import platform
import paxexpress_cli
from typer import Typer
from paxexpress_cli import (
    repo_cli,
    authentication_cli,
    package_cli,
    file_cli,
    version_cli,
)
from rich import print

system = platform.system()
if system in ["Darwin", "Windows"]:
    from keyring import set_keyring
if system == "Darwin":
    from keyring.backends import OS_X

    set_keyring(OS_X.Keyring())
elif system == "Windows":
    from keyring.backends import Windows

    try:
        import win32ctypes
    except ImportError:
        print("win32ctypes not found")
        print("try: \npip install pypiwin32")
        exit(1)

    set_keyring(Windows.WinVaultKeyring())
else:
    from keyring import set_keyring
    from keyrings.alt.file import PlaintextKeyring
    set_keyring(PlaintextKeyring())
    # automate platform detection
    pass
cli = Typer()

cli.add_typer(repo_cli, name="repository", help="work with repositories")
cli.add_typer(authentication_cli, name="auth", help="login and logout")
cli.add_typer(package_cli, name="package", help="Work with packages")
cli.add_typer(version_cli, name="version", help="Work with versions")
cli.add_typer(file_cli, name="file", help="Work with files")


self_cli = Typer(name="self")


@self_cli.command(help="Display cli tool version")
def version():
    print(paxexpress_cli.__version__)


cli.add_typer(self_cli, name="self")

def main():
    cli()

if __name__ == "__main__":
    cli()
