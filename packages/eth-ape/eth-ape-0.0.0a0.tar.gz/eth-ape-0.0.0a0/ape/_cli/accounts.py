import click


@click.group(short_help="Manage local accounts")
def cli():
    """
    Command-line helper for managing local accounts. You can unlock local accounts from
    scripts or the console using the accounts.load method.
    """


# Different name because `list` is a keyword
@cli.command(name="list", short_help="List available accounts")
def _list():
    pass


@cli.command(short_help="Add a new account by entering a private key")
@click.argument("id")
def new(id):
    pass


@cli.command(short_help="Add a new account with a random private key")
@click.argument("id")
def generate(id):
    click.echo("Generating a new private key...")


# Different name because `import` is a keyword
@cli.command(name="import", short_help="Import a new account via a keystore file")
@click.argument("id")
@click.argument("path", type=click.Path(exists=True, dir_okay=False, allow_dash=True))
def _import(id, path):
    pass


@cli.command(short_help="Export an existing account keystore file")
@click.argument("id")
@click.argument("path", type=click.Path(writable=True, allow_dash=True))
def export(id, path):
    pass


@cli.command(short_help="Change the password of an existing account")
@click.argument("id")
def password(id):
    pass


@cli.command(short_help="Delete an existing account")
@click.argument("id")
def delete(id):
    pass
