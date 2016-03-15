import base_test
import unittest
import getpass
import tempfile
from qmyf import crypt
from qmyf import common

class TestCrypt(base_test.BaseTest):

    password = common.get_password()

    def setUp(self):
        self.password = TestCrypt.password
        self.crypto_util = crypt.Crypt()

    def test_encrypt_decrypt(self):
        unencrypted = "Lorem ipsum"
        encrypted = self.crypto_util.encrypt(unencrypted)
        decrypted = self.crypto_util.decrypt(encrypted, self.password)
        self.assertEqual(unencrypted, decrypted)

    def test_encrypt_decrypt_json_to_file(self):
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.gpg')
        file_path = f.name
        data_json = {"foo": "bar"}
        self.crypto_util.encrypt_json_to_file(data_json, file_path)
        decrypted_data_json = self.crypto_util.decrypt_json_from_file(file_path, self.password)
        self.assertEqual(data_json['foo'], decrypted_data_json['foo'])

if __name__ == '__main__':
    unittest.main()
