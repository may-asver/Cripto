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
SIZE_NUMBER = 8
SIZE_BUFF = SIZE_NUMBER * 8


def create_Server():
    sock = socket.socket()  # Create socket
    sock.bind(SERVER_ADDR)
    sock.listen(1)
    while True:
        # Wait for a connection
        print('waiting for a connection')
        # Connect to client
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            file_name = connection.recv(SIZE_BUFF).decode()
            print(file_name)
            #filesize = int(connection.recv(SIZE_BUFF).decode())
            manage_file(file_name, connection)
            break
            # Clean up the connection
            connection.close()
        except Exception as e:
            print("Error on connection with server: ", e)


def manage_file(filename, connection):
    # Check if file exists
    while True:
        data = connection.recv(SIZE_BUFF)
        try:
            file = open(filename, "x")
            file.write(data.decode())
        except:
            file = open(filename, "w")
            file.write(data.decode())
        if not data:
            break
    file.close()



create_Server()
