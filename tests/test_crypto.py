import json
import os
import sys
import unittest

from django.conf import settings
from Crypto import Random

from crypto import generate_keypair, encrypt, decrypt, encrypt_json, decrypt_json, encrypt_telegraph, decrypt_telegraph


class TestCrypto(unittest.TestCase):
    """
    Unit test for module 'crypto'.
    """
    def setUp(self):
        _generate_public_and_private_key_if_not_exist()

    def tearDown(self):
        pass

    def testDecryptReversesEncrypt(self):
        text = Random.new().read(8)
        self.assertEqual(text, decrypt(encrypt(text)), "'decrypt' not reverses 'encrypt'")

    def testDecryptTelegraphReversesEncryptTelegraph(self):
        text = Random.new().read(500)
        self.assertEqual(text, decrypt_telegraph(encrypt_telegraph(text)), "'decrypt_telegraph' not reverses 'encrypt_telegraph'")

    def testDecryptJsonReversesEncryptJson(self):
        dt = {'name': 'jacksing', 'age': 35, 'address': ['1234567890',]}
        self.assertDictEqual(dt, decrypt_json(encrypt_json(dt)), "'decrypt_json' not reverses 'encrypt_json'")

    def testDotNetEncryptedCipher(self):
        dotNetCipher = """
fueQp1y5FpZhHkIho25Db6z8np/1DcIvTPWwRgfgUD+VIZfCkS8cBCdbGicNG+CxQSXyOHLhsLVI5nkhYyUkmjoe1hxk+EE/s80K1/8RgCA3fp9siE8Ccd4Z56loZ53Xiupv5lcxIbBJQsPe4qy+4AIXzevz6U6WIFZvfz4lt+U=
Ff2R1Eg60oadjy4ebDDVZW2nZKcd2bbtWtxv3IcVW2txHJTCJRjLQhTvprza9rocs2gUSmOpskodKo3gzt/1dHvyjSvX8RXcjj+nhL7jeZIyzY7ReBshPG24vZBn8tXRmTP/M1HfMYprrSJQFEilGkvuiLBAjmt7B55zj47kWqU=
blN14+8JYpfsxppIly+wUeP3De3KcDFOh7ZuJUR3HNPlxDQb1FXOH3xfShB3YkuKKnfAQO/rzfFxUmm6zD2h8xRYy/BWluCXnLQ0NevLXod4eISWg6QGCdzkj9nhQDcD3fQAejYA1sxpwpIEZSg2eXv7pbAqK7hAq/HlcHX1atM=
Ae79ZZMmR/qvBSc9wlML9Mbth4GzKCs7kWWqWLqSz0BHFfeZvNtNziwaIB0sfAOF5E0KJ3hJva8jf7o0s8wZ3QaGfv/GrOB01ALUj9PglYHBam7cLQKqhhCOXmhoH3Pd+h3cH39J+6Ch+qQ+MW1ADpoPKE5AzTqdChdmGaKHGM0=
M8R51Gf/TQ2ttR0a2BrKEmbKKNcxopPyDDv+72VozEbbxz0z3JZEvClnTRUb0Ok/ST2x0ly2sb/DEMdBESLpUr1+PgKLDITyClJggvHTceWD4jP8VZMg+aI5oN0v5QRjC2KxEh7vN726FCkE2oJOoTqTKAc4+5CtBQkS7oYCSpg=
cqApEqiuQzYHgzxQuWtgbEDD8lyCfE7E0QVEl72yF4SVpMQigfJMwNFzsyYBqE28A51pAbYNvmPCnZFigw9U3gEL89U5bfsZSlgmd0+FeeXQWlHbRDBWAKeB5v1DC8GsM6F/7UF5y2rIQazsRjS8Gvz9+pcW3gdNDl/Kh8E4DDU=
KV6E8cePUskASeFefnwlaIE5uNv3VpiK5bttGCgIDqFBbKimSvXdaEUsf9yBgdmCSsP3ntwxf66jh3s0hiwL48MFHDukbLkEkpfA+ds2ACRXQqgOWy5l/+QqQ5FFtYCLeURPZQV1PYBTnQYp20dYfbcFLOzxGZ5oNw+ehc0/MKA=
cehLZ9/x8rOyojJOEzNnj9JW0oPrUV2Tm6/1DazCRH67H/HM7nFRkYcjKLfJ89fp34Ly+UtdlcO3xqymVunHB4fIZ3Qrr5dHqxpaPfbjaiX8MOKJo9TV+OQ1jS3TvtsiitC0uStPZaykKqCcT/F0njKgJuOYZRMcsVwO4KTvK2g=
FWRP9flsQ+DgECNUnybRdnYteujJSY+2Qwus4GCHqTcQrLiakk/B+Hscrmf+parkwRLDKTRgKKNr8MpkHhGLYlg+uJrt8ZGRzXIrJOC8Wy89hEejj/IR6DSjcvlkCb+aq1+xPV4f0bE72Mm0Lh/eaK8fdrzA9yB0IOgtyHnuZEA=
Gpy1JX5a31e8nMIZgLVq/56AZM6LikqXHtf3PgRebOVGHiQ4LAZK+BcmYidpZ4GmA+80oOzmhAo9lDiguTQLnJb5N10wLmMZMm3cbeYMdvYCa+i5ywhySZ+tHtCxE2cRm5IgQSB9cQYSyH0ISpuesYXwzljKQVDvLWjBstjqN7E=
VNJJ8VEWT2cc/IyZ6kg0JUZOEfMV4wfRi//jsM0nMx9ZEF4yslQYloR+3sw17EhjQN6Ev6U1uQ2ieMY0HOCoHef/vWrO62CuKZj3qTPSVfbdFlfhl8iZV7+9I/CWy8zUJlpND0i3wjQPhQBHj+UPQtvqZanuZGbPli23JO5llzM=
aHabfTQtQ0NA2kWNXwIVisMDQRSxZELchqKK6PSIQ+sQ7Vljdoss0G2K8PlMw8D1P+bptHF/dt1g9qc016WGk1nAbKS8FdLlfe3nu6aduQL6viIVhedOPdLuvH5qGszDl3Vi0CUf4x7GcBikM6zt9tNKlL1OMfhtfnfe1nK+xtQ=
"""
        secret = 'Hello world - 1'
        for cipher in dotNetCipher.strip().split('\n'):
            self.assertEqual(secret, decrypt(cipher), 'decrypt dotnet encrypted string failed')

    def testDotNetEncryptedTelegraph(self):
        telegraphCipher = """
        eyJrZXkiOiJEcDg1Zm03c0U4Yk04T1ZIdGsyVGNiYWdmYmt2Znpxc043c1k5d3UvTTl3V0F3VUpzOGpabWE0ZCtUNkdZc1VBMTZmcXlJNU1GMXBNbUhaVC9YT2poSDJ5cTdXamV1SktqL21xTUNGMFMvU1hlTXdPckhRWGRPblZINlBEYkNhckE0OUpCUDRRd2ZJaVNXWmx0eGlVL2Q0dmtCWlpPVnVxQXVJZzdBRVZEc289IiwidGV4dCI6InY1YS9sSjJ5eXVEYVlncGxWWkhzVGdEbVdRR0VGdlBNRzNzbFFPMFZjUzQ9In0=
        """
        decrypted = decrypt_json(telegraphCipher.strip())
        print(decrypted)

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
        'testDecryptReversesEncrypt',
        'testDecryptJsonReversesEncryptJson',
        'testDecryptTelegraphReversesEncryptTelegraph'
    ]))


def get_test_dotnet_suite():
    return  unittest.TestSuite(map(TestCrypto, [
        'testDotNetEncryptedTelegraph',
        'testDotNetEncryptedCipher'
    ]))


def start():
    # suite = get_test_all_suite()
    suite = get_test_python_suite()
    # suite = get_test_dotnet_suite()
    unittest.TextTestRunner(verbosity=5).run(suite)
