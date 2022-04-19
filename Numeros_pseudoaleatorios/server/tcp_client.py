"""
    Script open a TCP client and print pseudorandom
    numbers.
    Author: Maya Aguirre.

    Date: 13/04/2022
"""
import socket
import readchar

# Global consts
PORT = 1000
SERVER_ADDR = ('localhost', PORT)
SIZE_NUMBER = 32
SIZE_BUFF = SIZE_NUMBER * 8


def client():
    sock = socket.socket()  # Create socket
    sock.connect(SERVER_ADDR)
    try:
        # Receive the number and print pseudorandom number on base64 format
        while True:
            send = readchar.readchar()
            sock.send(send)
            if send.decode() == '0':
                sock.close()
                break
            number_received = sock.recv(SIZE_BUFF)
            print(number_received.decode())
    except Exception as e:
        print("Error on client: ", e)
    finally:
        # Clean connection
        sock.close()


client()

