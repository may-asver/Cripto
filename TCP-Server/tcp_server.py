"""
    Script open a TCP server to receive a file.
    numbers.
    Author: Maya Aguirre.

    Date: 21/04/2022
"""
import socket

# Global consts
PORT = 1000
SERVER_ADDR = ('localhost', PORT)
SIZE_BUFF = 1024


def create_Server():
    sock = socket.socket()  # Create socket
    sock.bind(SERVER_ADDR)
    sock.listen(1)
    while True:
        # Wait for a connection
        print('waiting for a connection')
        try:
            # Connect to client
            connection, client_address = sock.accept()
            print('connection from', client_address)
            # Receive file
            file_name = connection.recv(SIZE_BUFF).decode()  # Receive file's name
            print(file_name)  # Show file's name
            manage_file(file_name, connection)  # Save file
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
            file.flush()
            file.close()
            break


create_Server()
