
import json
import os

from .fields import BaseField


class Env:
    """
    Class which captures all already validated and discovered environment
    variables.

    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        with open(Env.get_dump_filepath(), 'w') as f:
            f.write(json.dumps(kwargs))

    @classmethod
    def from_dump(cls):
        with open(Env.get_dump_filepath(), 'r') as f:
            return json.loads(f.read())

    @staticmethod
    def get_dump_filepath():
        base_dir = os.path.dirname(__file__)
        return f'{base_dir}/lily_env_dump.json'


class EnvParser:

    def __init__(self):

        env_variables = {}
        for field_name, field in self.fields.items():
            if field.required:
                raw_value = os.environ[field_name.upper()]

            else:
                raw_value = os.environ.get(
                    field_name.upper(), field.default)

            env_variables[field_name] = field.to_python(field_name, raw_value)

        self.env_variables = env_variables

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
        return Env(**self.env_variables)
