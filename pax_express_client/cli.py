import typer


app = typer.Typer()


@app.command()
def register(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def login(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def upload(name: str):
    typer.echo(f"Hello {name}")

if __name__ == "__main__":
    app()