"""
    Script open a TCP server to receive a signed and encrypted file.
    Author: Maya Aguirre.

    Date: 16/05/2022
"""
import socket
import os
from dotenv import load_dotenv
from argon2 import PasswordHasher as hasher
from proyecto_fin import main_encripted as decr
from proyecto_fin import signing as signing
from datetime import datetime

# Global consts
load_dotenv()
SERVER_ADDR = ('localhost', int(os.getenv("PORT"))) # Server address
SIZE_BUFF = int(os.getenv("SIZE_BUFF")) # Size of the buffer
KEY = bytes.fromhex(os.getenv("ENCRYPT_KEY"))  # Encryption key
SIGN_KEY_VERIFIED = os.getenv("PUBLIC_KEY")  # Public key


def main():
    try:
        conn = createConnection()
        user = conn.recv(SIZE_BUFF).decode('utf-8')  # Receive username
        psswd_hash = conn.recv(SIZE_BUFF).decode('utf-8')  # Receive hash
        login_verified = confirmLogin(conn, user, psswd_hash)
        if login_verified:  # Confirm login
            operation = int(conn.recv(SIZE_BUFF).decode('utf-8'))
            if operation == 1:  # Save encrypted file
                print("Saving signed and encrypted")
                saveEncryptedFile(conn)
            if operation == 2:  # Save decrypted file
                print("Saving unsigned and decrypted file")
                saveDecryptedFile(conn)
            if operation == 0:
                conn.close()
        else:
            confirmLogin(conn, user, psswd_hash)
    except Exception as e:
        with open('logs.txt', "a") as logsfile:
            today = datetime.now()
            logsfile.write(f"{today}: Error on server: {e}\n")


def createConnection():  # Create TCP connection
    sock = socket.socket()  # Create socket
    sock.bind(SERVER_ADDR)
    sock.listen(1)
    connection, client_address = sock.accept()  # Accept connection from client
    with open('logs.txt', "a") as logsfile:
        today = datetime.now()
        logsfile.write(f"{today}: Client connected: {client_address}\n")
    print("Connected: ", client_address)
    return connection


def confirmLogin(connection: socket, user, psswd_hash):  # Confirm login
    pswd = os.getenv("PASS")
    try:
        pswd_correct = True if hasher().verify(psswd_hash, pswd) else False # Verify password
        if user == os.getenv("USER") and pswd_correct:
            connection.send("True".encode('utf-8'))
            with open('logs.txt', "a") as logsfile:
                today = datetime.now()
                logsfile.write(f"{today}: Log in user: {user}\n")
            return True  # Login verified
    except Exception as e:
        connection.send("False".encode('utf-8'))
        with open('logs.txt', "a") as logsfile:  # Write log to logs.txt
            today = datetime.now()
            logsfile.write(f"{today}: Log in failed: {e}\n")
        return False  # Login failed


def saveEncryptedFile(con: socket):  # Save encrypted file
    filepath = con.recv(SIZE_BUFF).decode()  # Receive file's path
    path, file_name = os.path.split(filepath)
    file_name = "/" + file_name.split('.')[0] + "-encr." + file_name.split('.')[1]
    try:
        with open(path + file_name, "wb") as file:
            while True:
                data = con.recv(SIZE_BUFF)  # Receive data
                if not data:
                    break
                file.write(data)  # Save data
        with open('logs.txt', "a") as logsfile:
            today = datetime.now()
            logsfile.write(f"{today}: Encrypted File: {filepath}\n") # Save log
    except Exception as e:
        print("Error on server. Encryption: ", e)   # Error on server


def saveDecryptedFile(con: socket):  # Save decrypted file
    filepath = con.recv(SIZE_BUFF).decode('utf-8')  # Receive file's path
    path, file_name = os.path.split(filepath)
    file_name = "/" + file_name.split('.')[0] + "-decr." + file_name.split('.')[1]
    try:
        with open(path + file_name, "wb") as file:
            while True:
                data = con.recv(SIZE_BUFF)
                if not data:
                    break
                signed_check = signing.verifyMessage(data, SIGN_KEY_VERIFIED)
                if not signed_check:
                    break
                decrypted = decr.decrypt(signed_check, KEY)
                file.write(decrypted)
        with open('logs.txt', "a") as logsfile:
            today = datetime.now()
            logsfile.write(f"{today}: Decrypted and unsigned File: {filepath}\n")  # Save log
    except Exception as e:
        print("Failed decryption: ", e)  # Error on server
        with open('logs.txt', "a") as logsfile:
            today = datetime.now()
            logsfile.write(f"{today}: Save decrypted File failure: {e}\n")  # Save log


main()
