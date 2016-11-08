import json
import os
import sys
import unittest

sys.path.append('../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.conf import settings
from Crypto import Random

from crypto import generate_keypair, encrypt, decrypt, encrypt_json, decrypt_json


class TestCrypto(unittest.TestCase):
    """
    Unit test for module 'crypto'.
    """
    def setUp(self):
        generate_public_and_private_key_if_not_exist()

    def tearDown(self):
        pass

    def testDecryptReversesEncrypt(self):
        text = Random.new().read(8)
        self.assertEqual(text, decrypt(encrypt(text)), "'decrypt' not reverses 'encrypt'")

    def testDecryptJsonReversesEncryptJson(self):
        dt = {'name': 'jacksing', 'age': 35, 'address': ['1234567890',]}
        self.assertDictEqual(dt, json.loads(decrypt_json(encrypt_json(dt))), "'decrypt_json' not reverses 'encrypt_json'")


def generate_public_and_private_key_if_not_exist():
    prifile = settings.PRIKEY_FILENAME
    pubfile = settings.PUBKEY_FILENAME
    if not (os.path.exists(prifile) and os.path.exists(pubfile)):
        print('begin generate public and private key pair.')
        generate_keypair()
        print("generated public key file '%s' and private key file '%s'." % (pubfile, prifile))


def ras_decrypt_reverses_encrypt_with_8_bytes_data():
    text = Random.new().read(8)
    assert(text == decrypt(encrypt(text)))


def start():
    # generate_public_and_private_key_if_not_exist()
    # ras_decrypt_reverses_encrypt_with_8_bytes_data()

    unittest.main()

    # telegraph = encrypt_json()
    # print(telegraph)
    # receive = decrypt_json(telegraph)
    # print(json.dumps(json.loads(receive), indent=2))


if __name__ == '__main__':
    
    unittest.main()