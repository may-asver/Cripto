"""
    Script open a TCP client to send a file
    numbers.
    Author: Maya Aguirre.

    Date: 21/04/2022
"""
import socket

# Global consts
PORT = 1000
SERVER_ADDR = ('localhost', PORT)
SIZE_BUFF = 1024
FILENAME = "test.txt"


def client():
    sock = socket.socket()  # Create socket
    sock.connect(SERVER_ADDR)
    try:
        file = open("C:\\Users\\Maya\\Desktop\\" + FILENAME, "r")  # Read file
        sock.send(FILENAME.encode())  # Send filename
        data = file.read(SIZE_BUFF // 8)
        while data:
            sock.send(data.encode())
            data = file.read(SIZE_BUFF // 8)
        file.close()
    except Exception as e:
        print("Error on client: ", e)
    finally:
        # Clean connection
        print("File was send")
        sock.close()


client()
