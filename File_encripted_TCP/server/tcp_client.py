"""
    Script open a TCP client to send an encrypted file.
    Author: Maya Aguirre.

    Date: 26/04/2022
"""
import socket
import File_encripted_TCP.main_encripted as encr

# Global consts
PORT = 1500  # Port to connect
SERVER_ADDR = ('localhost', PORT)
SIZE_BUFF = 1024
FILENAME = "test2.txt"
KEY = encr.generate_key()


def client():
    sock = socket.socket()  # Create socket
    sock.connect(SERVER_ADDR)
    try:
        file = open(FILENAME, "r")  # Read file
        message = encr.encrypt(KEY, FILENAME.encode())
        sock.send(KEY)  # Send key to decrypt
        sock.send(message)  # Send filename
        data = file.read(SIZE_BUFF // 8)
        while data:
            encrypted = encr.encrypt(KEY, data.encode())
            sock.send(encrypted)
            data = file.read(SIZE_BUFF // 8)
        file.close()
    except Exception as e:
        print("Error on client: ", e)
    finally:
        # Clean connection
        print("File was send")
        sock.close()


client()
