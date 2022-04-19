"""
    Script open a TCP server and generate pseudorandom
    numbers.
    Author: Maya Aguirre.

    Date: 13/04/2022
"""
import socket
import Numeros_pseudoaleatorios.main_pseudo as pseudos

# Global consts
PORT = 1000
SERVER_ADDR = ('localhost', PORT)
SIZE_NUMBER = 32
SIZE_BUFF = SIZE_NUMBER * 8


def create_Server():
    sock = socket.socket()  # Create socket
    sock.bind(SERVER_ADDR)
    sock.listen(1)
    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            # Receive the data and send pseudorandom number
            while True:
                data = connection.recv(SIZE_BUFF)
                if data.decode() == '0':
                    connection.close()
                    print("connection closed")
                    break
                connection.send(pseudos.random_Number(SIZE_NUMBER))
        except Exception as e:
            print("Error on server: ", e)
        finally:
            # Clean up the connection
            connection.close()


create_Server()
