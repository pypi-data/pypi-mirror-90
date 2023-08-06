
import textwrap

from click.testing import CliRunner
from bash import bash

import szczypiorek as env
from szczypiorek.crypto import encrypt
from szczypiorek.cli import cli
from tests import BaseTestCase


class MyEnvParser(env.EnvParser):

    a = env.CharField()


my_env = None


class CliTestCase(BaseTestCase):

    def setUp(self):
        super(CliTestCase, self).setUp()
        self.runner = CliRunner()

    #
    # PRINT_ENV
    #
    def test_print_env(self):

        content = encrypt(textwrap.dedent('''
            a: b
        '''))
        self.root_dir.join('env.gpg').write(content, mode='w')

        global my_env
        my_env = MyEnvParser().parse()  # noqa

        result = self.runner.invoke(
            cli, ['print-env', 'tests.test_cli.my_env'])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            a: b
        ''').strip()

    #
    # ENCRYPT
    #
    def test_encrypt__no_yaml_files(self):

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 0
        assert result.output.strip() == ''

    def test_encrypt__some_yaml_files(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())
        self.root_dir.join('b.yml').write(textwrap.dedent('''
            a: whatever
        ''').strip())
        bash('git init')
        self.root_dir.join('.gitignore').write(
            '.szczypiorek_encryption_key\n'
            'a.yml\n'
            'b.yml\n'
        )

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.git')),
            str(self.root_dir.join('.gitignore')),
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('a.gpg')),
            str(self.root_dir.join('a.yml')),
            str(self.root_dir.join('b.gpg')),
            str(self.root_dir.join('b.yml')),
        ]

    def test_encrypt__some_error(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert 'Error: Well it seems that the' in result.output.strip()

    #
    # DECRYPT
    #
    def test_decrypt__no_gpg_files(self):

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])

        assert result.exit_code == 0
        assert result.output.strip() == ''

    def test_decrypt__some_gpg_files(self):

        content = encrypt(textwrap.dedent('''
            secret:
              key: secret.whatever
            is_important: true
            aws:
              url: {{ a.b.c }}

            number:
              of:
                workers: '113'
            a:
              b:
                c: http://hello.word.org
        '''))
        self.root_dir.join('env.gpg').write(content, mode='w')

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])
        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('env.gpg')),
            str(self.root_dir.join('env.yml')),
        ]

    def test_decrypt__some_error(self):

        self.root_dir.join('a.gpg').write('whatever')

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert (
            "Couldn't find the '.szczypiorek_encryption_key' file" in
            result.output.strip())
