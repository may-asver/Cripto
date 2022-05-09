"""
    Script to sign a file with PyNaCl

    Author: Maya Aguirre
    Date: May 5, 2022
"""

from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder


# Create a verified key
def generateVerifiedSign(sign_key):
    verified = sign_key.verify_key
    return verified.encode(encoder=HexEncoder)


def generateKey():
    key = SigningKey.generate()
    return key


def signMessage(key, message):
    signed = key.sign(message, encoder=HexEncoder)
    return signed


def verifyMessage(message, key):
    key_verified = verifyKey(key)
    if key_verified:
        verified = key_verified.verify(message, encoder=HexEncoder)
        if verified:
            return verified
    else:
        return False


def verifyKey(key: bytes):
    verify = VerifyKey(key, encoder=HexEncoder)
    if verify:
        return verify
    else:
        print("Sign key corrupted.")
        return False
