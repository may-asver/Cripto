"""
    Script open a TCP server to receive an encrypted file.
    Author: Maya Aguirre.

    Date: 26/04/2022
"""
import socket
import File_encripted_TCP.main_encripted as decr

# Global consts
PORT = 1500  # Port to listen
SERVER_ADDR = ('localhost', PORT)
SIZE_BUFF = 1024
COUNT: int = 0


def create_server():
    sock = socket.socket()  # Create socket
    sock.bind(SERVER_ADDR)
    sock.listen(1)
    while True:
        try:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            KEY = connection.recv(SIZE_BUFF // 8)
            print('connection from', client_address)
            file_name = decr.decrypt(connection.recv(SIZE_BUFF // 8), KEY).decode()  # Receive file's name and decrypt
            manage_file(file_name, connection, KEY)  # Save file
            connection.close()  # Clean up the connection
            break
        except Exception as e:
            print("Error on connection with server: ", e)


def manage_file(filename, connection, key):
    # Check if file exists
    data = connection.recv(SIZE_BUFF // 8)
    while data:
        decrypted = decr.decrypt(data, key)
        try:
            file = open(filename, "x")
            file.write(decrypted.decode())
        except:
            f_name = ""
            num = 0
            for letter in filename.split('.')[0]:
                if letter.isnumeric():
                    num = int(letter)
                    num += 1
                else:
                    f_name += letter
            extension = (str(num) + '.' + filename.split('.')[1])
            f_name += extension
            file = open(f_name, "w")
            file.write(decrypted.decode())
            print(f_name)
        data = connection.recv(SIZE_BUFF // 8)
        file.close()


create_server()
