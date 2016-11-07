from base64 import b64encode, b64decode

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5, DES
from Crypto.Cipher.DES import DESCipher
from Crypto.PublicKey import RSA
from django.conf import settings

from utils.checker import ensure_json_str, has_all_key
from utils.functions import random_str


try:
    PRIKEY_FILENAME = settings.PRIKEY_FILENAME
    PUBKEY_FILENAME = settings.PUBKEY_FILENAME
except AttributeError:
    PRIKEY_FILENAME = 'private.pem'
    PUBKEY_FILENAME = 'public.pem'


ENCRYPT_JSON_KEY_NAME = 'key'
ENCRYPT_JSON_CIPHER_NAME = 'text'


def encrypt_base64(func):
    def _encrypt_base64(*args):
        return b64encode(func(*args))
    return _encrypt_base64


def decrypt_base64(func):
    def _decrypt_base64(text, *args):
        return func(b64decode(text), *args)
    return _decrypt_base64


@encrypt_base64
def encrypt(text, pubkey_file=PUBKEY_FILENAME):
    with open(pubkey_file) as f:
        public_key = RSA.importKey(f.read())
        cipher = PKCS1_v1_5.new(public_key)
        return cipher.encrypt(text)


@decrypt_base64
def decrypt(text, prikey_file=PRIKEY_FILENAME):
    with open(prikey_file) as f:
        private_key = RSA.importKey(f.read())
        cipher = PKCS1_v1_5.new(private_key)
        return cipher.decrypt(text, 'decrypt falied')


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


@ensure_json_str
def encrypt_json(value, output='base64'):
    """
    Parse a json dict/str to an encrypt json in specified format.

    :Parameters:
      value: json dict/str
        json value to encript.
        accept a string object and the decorator does the ensure job.
      output: string
        output format in fields of base64/str/dict.
    """
    key = random_str()
    cipher = DESCipher(key).encrypt(value) # todo: jacksing> check whether needs parse to base64
    # cipher = b64encode(DESCipher(key).encrypt(value))

    result_dict = {
        ENCRYPT_JSON_KEY_NAME: encrypt(key),
        ENCRYPT_JSON_CIPHER_NAME: cipher,
    }

    if output == 'dict':
        return result_dict
    elif output == 'str':
        return json.dumps(result_dict)
    else:  # base64
        return b64encode(json.dumps(result_dict))


def decrypt_json(value, charset='base64', output=''):
    """
    Parse a string decrypted into json dict or string.
    """
    if charset == 'base64':
        value = b64decode(value)
    json_dict = json.loads(value)
    if not has_all_key(json_dict, [ENCRYPT_JSON_KEY_NAME, ENCRYPT_JSON_CIPHER_NAME]):
        return ValueError('Invalid json cipher.')

    key = json_dict[ENCRYPT_JSON_KEY_NAME]
    cipher = json_dict[ENCRYPT_JSON_CIPHER_NAME]  # todo: jacksing> needs to b64decode according to <encrypt_json>
    # cipher = b64decode(json_dict[ENCRYPT_JSON_CIPHER_NAME])
    return DESCipher(key).decrypt(cipher)


def start():
    # generate_keypair()
    # rstr = random_str()
    # print(rstr)
    # cipher = encrypt(rstr)
    # print(cipher)
    # print(decrypt(cipher))
    
    telegraph = encrypt_json({'name': 'jacksing', 'age': 35})
    receive = decrypt_json(telegraph)