"""
    Script open a TCP client to send an encrypted file.
    Author: Maya Aguirre.

    Date: 26/04/2022
"""
import socket
import Firmar_file_encrypted.main_encripted as encr
import Firmar_file_encrypted.signing as signfile

# Global consts
PORT = 1500  # Port to connect
SERVER_ADDR = ('localhost', PORT)
SIZE_BUFF = 4096
FILENAME = "test2.txt"
KEY = encr.generate_key()  # Key to encrypt
SIGN_KEY = signfile.generateKey()  # Private key
SIGN_KEY_VERIFIED = signfile.generateVerifiedSign(SIGN_KEY)  # Public key


def client():
    sock = socket.socket()  # Create socket
    sock.connect(SERVER_ADDR)
    try:
        file = open(FILENAME, "r", encoding='latin-1')  # Read file
        message = signfile.signMessage(SIGN_KEY, FILENAME.encode())
        sock.send(KEY)  # Send key to decrypt
        sock.send(SIGN_KEY_VERIFIED)  # Send sign key
        sock.send(encr.encrypt(KEY, message))  # Send filename
        data = file.read(SIZE_BUFF)
        while data:
            packet = signfile.signMessage(SIGN_KEY, data.encode())
            encrypted = encr.encrypt(KEY, packet)
            sock.send(encrypted)
            data = file.read(SIZE_BUFF)
        file.close()
    except Exception as e:
        print("Error on client: ", e)
    finally:
        # Clean connection
        print("File was send")
        sock.close()


client()
