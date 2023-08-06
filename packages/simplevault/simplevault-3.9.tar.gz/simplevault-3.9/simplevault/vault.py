import json
import os.path
import sys

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Vault:
    """
    Vault is a cyphered dict saved on disk in a single file
    """

    def __init__(self, password=None, path="vault.db"):
        self.path = path
        self.password = password
        self.vault = None

        if password is not None:
            self.__load(path=path, password=password)

    def __load(self, path, password):
        try:
            b64 = ""
            with open(path, "r") as vault_file:
                b64 = json.load(vault_file)

            nonce = b64decode(b64["nonce"])
            tag = b64decode(b64["tag"])
            data = b64decode(b64["data"])
            cipher = AES.new(b64decode(password), AES.MODE_EAX, nonce=nonce)
            raw_data = cipher.decrypt(data)

            cipher.verify(tag)
            self.vault = json.loads(raw_data)

        except FileNotFoundError:
            print(f"Could not load file {path}")

    def view(self):
        print(json.dumps(self.vault, indent=2))

    def keygen(self):
        return b64encode(get_random_bytes(32)).decode()

    def create(self, force=False):
        assert isinstance(force, bool)

        if force is False and os.path.exists(self.path):
            print("Vault already exists")
            return None

        if self.password is None:
            self.password = self.keygen()

        # add entropy to file
        self.vault = {self.keygen(): self.keygen()}

        self.save()
        return self.password

    def get(self, key, default=None):
        value = self.vault.get(key, default)
        if isinstance(value, str):
            try:
                return json.loads(value)
            except ValueError:
                return value

        return value

    def load(self, source=None):
        """
        Import a json into the vault
        Args:
        source if None read for stdin otherwise expects a json filepath
        """
        if source is None:
            source_string = sys.stdin.read()
        else:
            source_string = open(source, "r").read()

        self.vault.update(json.loads(source_string))
        self.save()

    def update(self, key, value):
        self.vault.update({key: value})
        self.save()

    def remove(self, key):
        del self.vault[key]
        self.save()

    def save(self):
        cipher = AES.new(b64decode(self.password), AES.MODE_EAX)
        nonce = cipher.nonce
        to_cipher = json.dumps(self.vault).encode()
        ciphertext, tag = cipher.encrypt_and_digest(to_cipher)
        result = json.dumps(
            {
                "nonce": b64encode(nonce).decode(),
                "tag": b64encode(tag).decode(),
                "data": b64encode(ciphertext).decode(),
            }
        )
        with open(self.path, "w") as vault_file:
            vault_file.write(result)
