import json

from crypto import generate_keypair, encrypt, decrypt, encrypt_json, decrypt_json

def start():
    generate_keypair()
    rstr = random_str()
    print(rstr)
    cipher = encrypt(rstr)
    print(cipher)
    print(decrypt(cipher))
    
    telegraph = encrypt_json({'name': 'jacksing', 'age': 35, 'address': ['1234567890',]})
    print(telegraph)
    receive = decrypt_json(telegraph)
    print(json.dumps(json.loads(receive), indent=2))
