
import string
import random
import os
from datetime import datetime
import json
import base64

import gnupg

from .git import assert_is_git_repository, assert_is_git_ignored
from .exceptions import (
    DecryptionError,
    EncryptionKeyFileMissingError,
    EncryptionKeyBrokenBase64Error,
    EncryptionKeyBrokenJsonError,
    EncryptionKeyTooShortError,
)
from .constants import (
    ENCRYPTION_KEY_FILE,
    ENCRYPTION_KEY_ENV,
    ENCRYPTION_KEY_LENGTH,
)


def encrypt(content, key_filepath=None):
    gpg = gnupg.GPG()

    create_encryption_key_if_not_exist(key_filepath)
    return str(
        gpg.encrypt(
            content,
            symmetric='AES256',
            passphrase=get_encryption_key(key_filepath),
            recipients=None))


def decrypt(content, key_filepath=None):
    gpg = gnupg.GPG()

    decrypted = gpg.decrypt(
        content,
        passphrase=get_encryption_key(key_filepath))

    if decrypted.ok:
        return str(decrypted)

    else:
        raise DecryptionError("""
            Something went wrong while attempting to decrypt. The big chance
            is that you've used broken encryption key.

            Therefore if you see this message it means that you're trying to
            do something bad. Stop doing that.
        """)


def get_encryption_key(key_filepath=None):

    try:
        encryption_key = None

        # -- only attempt reading from ENV if key not explicitly set
        if not key_filepath:
            encryption_key = os.environ.get(ENCRYPTION_KEY_ENV)
            encryption_key_source = f"'{ENCRYPTION_KEY_ENV}' environment variable"  # noqa

        if not encryption_key:
            # -- if key file path not given take default one
            if not key_filepath:
                key_filepath = ENCRYPTION_KEY_FILE

            encryption_key_source = f"'{key_filepath}' file"
            with open(key_filepath, 'rb') as f:
                encryption_key = f.read()

        encryption_key = base64.b64decode(encryption_key).decode('utf8')
        encryption_key = json.loads(encryption_key)['key']

    except FileNotFoundError:
        raise EncryptionKeyFileMissingError(f"""
            Couldn't find the {encryption_key_source}. It is required
            for the correct functioning of the encryption and decryption
            phases.

            If you see this message while performing 'decrypt' then
            simply request the file from fellow code contributor.
            In the 'encrypt' scenario the file is created automatically.
        """)

    except base64.binascii.Error:
        raise EncryptionKeyBrokenBase64Error(f"""
            The content of the {encryption_key_source} was automatically
            encoded with base64 so that noone tries to mess around with it.
            So if you see this message that means that someone tried just that.

            Try to get access to the not broken version of the
            {encryption_key_source} or if you have access to the not
            encrypted version you environment files simply remove the broken
            file and run 'decrypt' phase one more time.
        """)

    except (KeyError, json.decoder.JSONDecodeError):
        raise EncryptionKeyBrokenJsonError(f"""
            The content of the {encryption_key_source} must be a valid
            json file encoded with base64. It takes the following shape:

            {{
                "key": <autmatically generated secret>,
                "created_datetime": <iso datetime of the key creation>
            }}
        """)

    if assert_is_git_repository():
        assert_is_git_ignored(key_filepath)

    if len(encryption_key) < ENCRYPTION_KEY_LENGTH:
        raise EncryptionKeyTooShortError(f"""
            So it seems that the key used for encryption hidden in
            the {encryption_key_source} is too short.

            Which means that because of some reason you've decided to mess
            around with the built-in generator of the secured key.

            Try to get access to the not broken version of the
            {encryption_key_source} or if you have access to the not
            encrypted version you environment files simply remove the broken
            file and run 'decrypt' phase one more time.
        """)

    return encryption_key


def create_encryption_key_if_not_exist(key_filepath=None):

    if not key_filepath:
        key_filepath = ENCRYPTION_KEY_FILE

    if os.path.exists(key_filepath):
        return False

    with open(key_filepath, 'wb') as f:
        content = {
            'key': ''.join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=ENCRYPTION_KEY_LENGTH)),
            'created_datetime': datetime.utcnow().isoformat(),
        }
        content = json.dumps(content)
        content = content.encode('utf8')
        content = base64.b64encode(content)

        f.write(content)

    return True
