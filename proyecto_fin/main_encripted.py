"""
    Script to send a file encrypted with AES-256.
    Author: Maya Aguirre

    Date: 26/04/2022
"""

import nacl.secret as ncsecret
import nacl.utils as ncutils
from nacl.encoding import HexEncoder

# Global consts
SIZE_KEY = 32  # 32 bytes = 256 bits


def generate_key():
    secret_key = ncutils.random(SIZE_KEY)  # Generates a random key
    return secret_key


def encrypt(key: bytes, message: bytes):  # Encrypts the message with AES-256
    box = ncsecret.SecretBox(key)  # Creates a secret box
    encrypted = box.encrypt(message, encoder=HexEncoder)  # Encrypts the message
    return encrypted


def decrypt(message: bytes, key: bytes):  # Decrypts the message with AES-256
    box = ncsecret.SecretBox(key)  # Creates a secret box
    decrypted = box.decrypt(message, encoder=HexEncoder)  # Decrypts the message
    return decrypted
