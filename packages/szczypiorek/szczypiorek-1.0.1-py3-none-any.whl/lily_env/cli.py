
import click

from .parser import Env


@click.group()
def cli():
    """Expose multiple commands allowing one to work with lily_env."""
    pass


@click.command()
def dump():
    """
    Dump currently loaded env variables into a console.

    """

    try:
        click.echo('\n'.join([
            f'{k.upper()}: {v}' for k, v in Env.from_dump().items()]))

    except FileNotFoundError:
        raise click.ClickException(
            'Dump file does not exist, run `parse` on your '
            '`EnvParser` instance in order to render it')


cli.add_command(dump)
