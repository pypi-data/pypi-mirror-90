
from glob import glob
import os
import re
import importlib

import click

from .utils import load_yaml
from .git import assert_is_git_ignored
from .exceptions import BaseException
from . import crypto


@click.group()
def cli():
    """Expose multiple commands allowing one to work with szczypiorek."""
    pass


@click.command()
@click.argument('env_path')
def print_env(env_path):
    """Print currently loaded env variables into stdout."""

    env_path_parts = env_path.split('.')
    env_path = '.'.join(env_path_parts[:-1])
    env_variable = env_path_parts[-1]

    env = getattr(importlib.import_module(env_path), env_variable)
    click.echo('\n'.join([f'{k}: {v}' for k, v in env.env.items()]))


@click.command()
@click.argument('path')
@click.option('--key_filepath', '-k')
def encrypt(path, key_filepath=None):
    """Encrypt all yml files in a given path."""

    if os.path.isdir(path):
        filepaths = sorted(
            glob(os.path.join(path, '*.yml')) +
            glob(os.path.join(path, '*.yaml')))

    else:
        filepaths = [path]

    for filepath in filepaths:
        with open(filepath, 'r') as f:
            gpg_filepath = re.sub(r'(\.yml|\.yaml)', '.gpg', filepath)

            with open(gpg_filepath, 'w') as g:
                click.secho(f'[ENCRYPTING] {filepath}', color='green')

                try:
                    assert_is_git_ignored(filepath)

                    content = f.read()
                    # -- used here only to validate
                    load_yaml(content)
                    g.write(crypto.encrypt(content, key_filepath))

                except BaseException as e:
                    raise click.ClickException(e.args[0])


@click.command()
@click.argument('path')
@click.option('--key_filepath', '-k')
def decrypt(path, key_filepath=None):
    if os.path.isdir(path):
        filepaths = glob(os.path.join(path, '*.gpg'))

    else:
        filepaths = [path]

    for filepath in filepaths:
        with open(filepath, 'r') as f:
            yml_filepath = filepath.replace('.gpg', '.yml')
            with open(yml_filepath, 'w') as g:
                click.secho(f'[DECRYPTING] {filepath}', color='green')

                try:
                    g.write(crypto.decrypt(f.read(), key_filepath))

                except BaseException as e:
                    raise click.ClickException(e.args[0])


cli.add_command(encrypt)
cli.add_command(decrypt)
cli.add_command(print_env)
