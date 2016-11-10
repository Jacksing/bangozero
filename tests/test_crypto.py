# encoding: utf-8

from base64 import b64encode, b64decode
import json
import os
import sys
import unittest

from django.conf import settings
from Crypto import Random

from crypto import \
    CSCrypto, generate_keypair, encrypt, decrypt, \
    encrypt_json, decrypt_json, encrypt_telegraph, decrypt_telegraph
from utils.functions import random_str


class TestCrypto(unittest.TestCase):
    """
    Unit test for module 'crypto'.
    """
    def setUp(self):
        _generate_public_and_private_key_if_not_exist()

    def tearDown(self):
        pass

    def test_encrypt_circuit(self):
        text = Random.new().read(10)
        cipher = encrypt('text')
        flyback = decrypt(cipher)
        self.assertEqual(text, decrypt(encrypt(text)), "'decrypt' not reverses 'encrypt'")

    def test_encrypt_telegraph_circuit(self):
        text = Random.new().read(500)
        # text = random_str(500).encode('utf-8')
        self.assertEqual(
            text, decrypt_telegraph(encrypt_telegraph(text)),
            "'decrypt_telegraph' not reverses 'encrypt_telegraph'")

    def test_encrypt_json_circuit(self):
        dt = {'name': 'jacksing', 'age': 35, 'address': ['1234567890',]}
        self.assertDictEqual(dt, decrypt_json(encrypt_json(dt)), "'decrypt_json' not reverses 'encrypt_json'")

    def test_cs_encrypt(self):
        secret = random_str(10)
        self.assertEqual(secret, decrypt(CSCrypto().encrypt(secret)), "'decrypt' not reverses 'cs_encrypt'")

    def test_cs_decrypt(self):
        secret = random_str(10)
        self.assertEqual(secret, CSCrypto().decrypt(encrypt(secret)), "'cs_decrypt' not reverses 'encrypt'")

    def test_cs_encrypt_telegraph(self):
        telegraph = random_str(500)
        self.assertEqual(
            telegraph, decrypt_telegraph(CSCrypto().encrypt_telegraph(telegraph)),
            "'decrypt_telegraph' not reverses 'cs_encrypt_telegraph'")

    def test_cs_decrypt_telegraph(self):
        telegraph = random_str(500)
        self.assertEqual(
            telegraph, CSCrypto().decrypt_telegraph(encrypt_telegraph(telegraph)),
            "'cs_decrypt_telegraph' not reverses 'encrypt_telegraph'")

    def test_cs_encrypt_circuit(self):
        text = random_str(10)
        self.assertEqual(text, CSCrypto().decrypt(CSCrypto().encrypt(text)), "'cs_decrypt' not reverses 'cs_encrypt'")

    def test_cs_encrypt_telegraph_circuit(self):
        text = random_str(500)
        self.assertEqual(
            text, CSCrypto().decrypt_telegraph(CSCrypto().encrypt_telegraph(text)),
            "'cs_decrypt_telegraph' not reverses 'cs_encrypt_telegraph'")


def _generate_public_and_private_key_if_not_exist():
    prifile = settings.PRIKEY_FILENAME
    pubfile = settings.PUBKEY_FILENAME
    if not (os.path.exists(prifile) and os.path.exists(pubfile)):
        print('begin generate public and private key pair.')
        generate_keypair()
        print("generated public key file '%s' and private key file '%s'." % (pubfile, prifile))


def get_test_all_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestCrypto)


def get_test_python_suite():
    return unittest.TestSuite(map(TestCrypto, [
        'test_encrypt_circuit',
        'test_encrypt_telegraph_circuit',
        'test_encrypt_json_circuit',
    ]))


def get_test_dotnet_suite():
    return  unittest.TestSuite(map(TestCrypto, [
        'test_cs_encrypt_circuit',
        'test_cs_encrypt_telegraph_circuit',
    ]))


def get_test_py_interact_with_cs():
    return  unittest.TestSuite(map(TestCrypto, [
        'test_cs_encrypt',
        'test_cs_decrypt',
        'test_cs_encrypt_telegraph',
        'test_cs_decrypt_telegraph',
    ]))


def start():
    suite = get_test_all_suite()
    # suite = get_test_python_suite()
    # suite = get_test_dotnet_suite()
    # suite = get_test_py_interact_with_cs
    unittest.TextTestRunner(verbosity=1).run(suite)
