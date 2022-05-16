"""
    Script to sign a file with PyNaCl

    Author: Maya Aguirre
    Date: May 5, 2022
"""

from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder


# Create a verified key
def generateVerifiedSign(sign_key: str):
    sign_key = bytes.fromhex(sign_key)
    verified = SigningKey(sign_key).verify_key.encode()
    return verified.hex()


def signMessage(key: str, message): # key is hex
    key = bytes.fromhex(key)
    sign_key = SigningKey(key)
    signed = sign_key.sign(message, encoder=HexEncoder)
    return signed


def verifyMessage(message, key): # key is hex
    key = bytes.fromhex(key)
    key_verified = verifyKey(key)
    if key_verified:
        verified = key_verified.verify(message, encoder=HexEncoder)
        if verified:
            return verified
    else:
        return False


def verifyKey(key: bytes): # key is hex
    verify = VerifyKey(key)
    if verify:
        return verify
    else:
        print("Sign key corrupted.")
        return False
