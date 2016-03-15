import gnupg
from path import Path
import json

class Crypt:
    def __init__(self, config = None):
        if not config:
            f = open('config.json', 'r')
            data = f.read()
            f.close()
            config = json.loads(data)

        self.config = config
        self.gpg = gnupg.GPG(homedir=config['gpghomedir'], binary=config['gpgbinary'])

    def encrypt(self, message):
        return str(self.gpg.encrypt(message, self.config['gpgkeyname']))

    def decrypt(self, encrypted_message, passphrase):
        decrypted_message = self.gpg.decrypt(encrypted_message, passphrase=passphrase)
        if decrypted_message.ok:
            return decrypted_message.data
        else:
            print decrypted_message.stderr
            return

    def encrypt_json_to_file(self, data_as_json, target_path):
        file_path = Path(target_path)
        if not file_path.ext or file_path.ext != '.gpg':
            file_path.ext = '.gpg'

        data_as_str = json.dumps(data_as_json)
        encrypted_data = unicode(self.encrypt(data_as_str))
        f = file_path.open('w')
        f.write(encrypted_data)
        f.flush()
        f.close()

    def decrypt_json_from_file(self, source_path, passphrase):
        f = open(source_path, 'r')
        encrypted_data_str = f.read()
        f.close()
        data_str = self.decrypt(encrypted_data_str, passphrase)
        return json.loads(data_str)
