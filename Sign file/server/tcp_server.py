"""
    Script open a TCP server to receive an encrypted file.
    Author: Maya Aguirre.

    Date: 26/04/2022
"""
import socket
import Firmar_file_encrypted.main_encripted as decr
import Firmar_file_encrypted.signing as signing

# Global consts
PORT = 1500  # Port to listen
SERVER_ADDR = ('localhost', PORT)
SIZE_BUFF = 4096


def create_server():
    sock = socket.socket()  # Create socket
    sock.bind(SERVER_ADDR)
    sock.listen(1)
    while True:
        try:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            KEY = connection.recv(SIZE_BUFF)  # Key to decrypt
            SIGN_KEY = connection.recv(SIZE_BUFF)  # Sign key
            if not SIGN_KEY:
                connection.close()
                break
            print('connection from', client_address)
            # Receive file's name and decrypt
            check = signing.verifyMessage(decr.decrypt(connection.recv(SIZE_BUFF), KEY), SIGN_KEY)
            file_name = check.decode('windows-1252', "replace") if check else ""
            if not file_name:
                print("Sign key failure")
                connection.close()
                break
            manage_file(file_name, connection, KEY, SIGN_KEY)  # Save file
            connection.close()  # Clean up the connection
            break
        except Exception as e:
            print("Error on connection with server: ", e)
            connection.close()
            break


def manage_file(filename, connection, key, sign_key):
    # Check if file exists
    data = connection.recv(SIZE_BUFF)
    verified = signing.verifyMessage(decr.decrypt(data, key), sign_key)
    while verified:
        try:
            file = open(filename, "x")
            file.write(verified.decode('windows-1252', 'replace'))
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
            file.write(verified.decode('windows-1252', 'replace'))
            print(f_name)
        data = connection.recv(SIZE_BUFF)
        verified = signing.verifyMessage(decr.decrypt(data, key), sign_key)
        file.close()


create_server()
