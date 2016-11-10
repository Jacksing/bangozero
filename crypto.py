# encoding: utf-8
#
#  Encrypt and decrypt telegraph.
#
# Written in 2016 by Jacksing Tang <iterrole@163.com>
# 
# ===================================================================
# The contents of this file are defined to apply a cryptography to
# make security for a kind of mail payload called 'telegraph' while
# it is transported by mail.
# 
# As the cryptography may be used in DotNet environment, here also
# applys a 'CSCrypto' class which written in C# to support the scene.
# ===================================================================

import os
import json
from base64 import b64encode, b64decode

from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP as PKCS1_v1_5, AES
from Crypto.Cipher.AES import AESCipher
from Crypto.PublicKey import RSA
from django.conf import settings

from utils.checker import ensure_json_str, has_all_key
from utils.functions import execmd


try:
    PRIKEY_FILENAME = settings.PRIKEY_FILENAME
    PUBKEY_FILENAME = settings.PUBKEY_FILENAME
except AttributeError:
    PRIKEY_FILENAME = 'private.pem'
    PUBKEY_FILENAME = 'public.pem'


ENCRYPT_TELEGRAPH_KEY_NAME = 'key'
ENCRYPT_TELEGRAPH_CIPHER_NAME = 'text'

AES_PADDING = '\0'
AES_CIPHER_MODE = AES.MODE_CFB
AES_KEY_SIZE = AES.block_size


def output_base64(func):
    def _output_base64(*args):
        return b64encode(func(*args))
    return _output_base64


def input_base64(func):
    def _input_base64(text, *args):
        return func(b64decode(text), *args)
    return _input_base64


@output_base64
def encrypt(secret, pubkey_file=PUBKEY_FILENAME):
    with open(pubkey_file) as f:
        public_key = RSA.importKey(f.read())
        rsa = PKCS1_v1_5.new(public_key)
        return rsa.encrypt(secret)


@input_base64
def decrypt(cipher, prikey_file=PRIKEY_FILENAME):
    with open(prikey_file) as f:
        private_key = RSA.importKey(f.read())
        rsa = PKCS1_v1_5.new(private_key)
        return rsa.decrypt(cipher)


def generate_keypair():
    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)

    private_key = rsa.exportKey()
    public_key = rsa.publickey().exportKey()
    try:
        with open(PRIKEY_FILENAME, 'w') as f:
                f.write(private_key)
        with open(PUBKEY_FILENAME, 'w') as f:
            f.write(public_key)
    except IOError as ex:
        raise ex


def encrypt_telegraph(secret):
    """
    Encrypt 'secret' with AES encryption and get its key and iv RSA encrypted.
    Return a key and IV self-including cipher string.

    :Parameters:
      secret: string
        string to encrypt.
      output: string
        string in base64.
    """
    secret += AES_PADDING * (AES.block_size - len(secret) % AES.block_size)
    key = Random.new().read(AES_KEY_SIZE)
    iv = Random.new().read(AES_KEY_SIZE)
    cipher = AESCipher(key, AES_CIPHER_MODE, iv).encrypt(secret)

    result_dict = {
        ENCRYPT_TELEGRAPH_KEY_NAME: encrypt(b64encode(key + iv)),
        ENCRYPT_TELEGRAPH_CIPHER_NAME: b64encode(cipher),
    }

    return b64encode(json.dumps(result_dict))


@ensure_json_str
def encrypt_json(secret):
    """
    Encrypt a json string 'secret' with AES encryption and get its key and iv RSA encrypted.

    :Parameters:
      secret: json string
        json secret to encrypt.
        accept a string object and the decorator does the ensure job.
      output: string
        string in base64.
    """
    return encrypt_telegraph(secret)


def decrypt_telegraph(cipher):
    """
    Decrypt key and IV self-including 'cipher' into secret string.
    """
    json_dict = json.loads(b64decode(cipher))
    if not has_all_key(json_dict, [ENCRYPT_TELEGRAPH_KEY_NAME, ENCRYPT_TELEGRAPH_CIPHER_NAME]):
        return ValueError('Invalid telegraph cipher.')

    key = b64decode(decrypt(json_dict[ENCRYPT_TELEGRAPH_KEY_NAME]))  # combined with key + iv
    iv = key[AES_KEY_SIZE:]
    key = key[0:AES_KEY_SIZE]
    
    telegraph_cipher = b64decode(json_dict[ENCRYPT_TELEGRAPH_CIPHER_NAME])
    return AESCipher(key, AES_CIPHER_MODE, iv).decrypt(telegraph_cipher).rstrip(AES_PADDING)


def decrypt_json(cipher):
    return json.loads(decrypt_telegraph(cipher))


class CSCrypto:
    _EXECUTOR = "D:/Work/bangoinfinite/telec/bin/Debug/telec.exe"

    def __init__(self, *args, **kwargs):
        if not os.path.exists(self._EXECUTOR):
            raise EnvironmentError('cannot find a cmd line executor.')
    
    def encrypt(self, secret, pubkey_file=PUBKEY_FILENAME):
        return execmd('%s rsa %s' % (self._EXECUTOR, secret))

    def decrypt(self, cipher, prikey_file=PRIKEY_FILENAME):
        return execmd('%s drsa %s' % (self._EXECUTOR, cipher))

    def encrypt_telegraph(self, secret, pubkey_file=PUBKEY_FILENAME):
        return execmd('%s aes %s' % (self._EXECUTOR, secret))

    def decrypt_telegraph(self, cipher, prikey_file=PRIKEY_FILENAME):
        return execmd('%s daes %s' % (self._EXECUTOR, cipher))
