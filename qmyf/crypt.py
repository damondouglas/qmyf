import gnupg

class Crypt:
    def __init__(self, config):
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
