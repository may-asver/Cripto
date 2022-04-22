"""
    Script open a TCP client and print pseudorandom
    numbers.
    Author: Maya Aguirre.

    Date: 13/04/2022
"""
import socket

# Global consts
PORT = 1000
SERVER_ADDR = ('localhost', PORT)
SIZE_NUMBER = 8
SIZE_BUFF = SIZE_NUMBER * 8
FILENAME = "test.txt"


def client():
    sock = socket.socket()  # Create socket
    sock.connect(SERVER_ADDR)
    try:
        # Receive the number and print pseudorandom number on base64 format
        file = open("C:\\Users\\Maya\\Desktop\\" + FILENAME, "r")
        sock.send(FILENAME.encode())  # Send filename
        # size_file = os.path.getsize("C:\\Users\\Maya\\Desktop\\"+FILENAME)
        # sock.send(size_file)
        while True:
            data = file.read(SIZE_BUFF)
            sock.send(data.encode())
            if not data:
                break
        file.close()
    except Exception as e:
        print("Error on client: ", e)
    finally:
        # Clean connection
        print("File was send")
        sock.close()


client()
