
import os

import click

from .fields import BaseField
from .crypto import decrypt
from .utils import load_yaml, flatten, substitute


class Env:

    def __init__(self, **env):
        for k, v in env.items():
            setattr(self, k, v)

        self.env = env


class EnvParser:

    _envs_cache = {}

    @property
    def fields(self):
        fields = {}
        for name in dir(self):
            if name != 'fields':
                attr = getattr(self, name)
                if isinstance(attr, BaseField):
                    fields[name] = attr

        return fields

    def parse(self):
        env_path = os.environ.get('SZCZYPIOREK_PATH', 'env.gpg')
        env_key = (
            f'{self.__class__.__module__}.'
            f'{self.__class__.__name__}.'
            f'{env_path}')

        _env = EnvParser._envs_cache.get(env_key)

        if not _env:
            click.secho(f'[LOADING] {env_path}', color='green')
            with open(env_path, 'r') as f:
                env = decrypt(f.read())
                env = load_yaml(env)
                env = flatten(env)
                env = substitute(env)

            env_variables = {}
            for field_name, field in self.fields.items():
                if field.required:
                    raw_value = env[field_name]

                else:
                    raw_value = env.get(field_name, field.default)

                env_variables[field_name] = (
                    field.to_python(field_name, raw_value))

                if field.as_env:
                    if isinstance(field.as_env, str):
                        env_name = field.as_env

                    else:
                        env_name = field_name.upper()

                    os.environ[env_name] = env_variables[field_name]

                if field.as_file:
                    if isinstance(field.as_file, str):
                        file_name = field.as_file

                    else:
                        file_name = field_name

                    with open(file_name, 'w') as f:
                        f.write(env_variables[field_name])

            EnvParser._envs_cache[env_key] = Env(**env_variables)

        return EnvParser._envs_cache[env_key]
