"""
    Script open a TCP client to send a signed and encrypted file.
    Author: Maya Aguirre.

    Date: 16/05/2022
"""
import socket
import os
from dotenv import load_dotenv
from proyecto_fin import main_encripted as encr
from proyecto_fin import signing as signfile
from proyecto_fin import main as menu
import wx as wx
from datetime import datetime

# Global consts
load_dotenv()
SERVER_ADDR = ('localhost', int(os.getenv("PORT")))
KEY = bytes.fromhex(os.getenv("ENCRYPT_KEY"))  # Key to encrypt
SIGN_KEY = os.getenv("PRIV_KEY")  # Private key
SIGN_KEY_VERIFIED = signfile.generateVerifiedSign(SIGN_KEY)  # Public key
SIZE_BUFF = int(os.getenv("SIZE_BUFF"))
BUFF_FILE = int(os.getenv("BUFF_FILE"))


def main():
    try:
        conn = createConnection()
        user, psswd = menu.login_menu()
        conn.send(user.encode('utf-8'))  # Send username to server
        conn.send(psswd.encode('utf-8'))  # Send hash to server
        login_verified = conn.recv(SIZE_BUFF).decode()  # Get answer from server
        if login_verified == "True":  # Operations menu
            operation = menu.menu_operations()
            conn.send(str(operation).encode())  # Send operation to server
            if operation == 1:  # Encrypt file and save it
                filepath = fileExplorer('*')
                encrypt(conn, filepath)
            if operation == 2:
                filepath = fileExplorer('*')
                decrypt(conn, filepath)
            if operation == 0:
                print("Exiting...")
                conn.close()
        else:
            print("User or password wrong. Try again.")
            with open('logs_client.txt', "a") as logsfile:
                today = datetime.now()
                logsfile.write(f"{today}: Log in failure: {user}\n")
            menu.login_menu()
    except Exception as e:
        with open('logs_client.txt', "a") as logsfile:
            today = datetime.now()
            logsfile.write(f"{today}: Error on client: {e}\n")


def createConnection():  # Create connection with server
    sock = socket.socket()  # Create socket
    sock.connect(SERVER_ADDR)
    return sock


def encrypt(connection: socket, filepath):  # Encrypt file and send it to server
    connection.send(filepath.encode('utf-8'))  # Send file path to server
    print("Encrypting and signing")
    try:
        with open(filepath, "rb") as file:
            while True:
                data = file.read(BUFF_FILE)
                if not data:
                    break
                encrypted = encr.encrypt(KEY, data)
                signed = signfile.signMessage(SIGN_KEY, encrypted)  # Sign file
                connection.sendall(signed)  # Send encrypted and signed file to server
        with open('logs_client.txt', "a") as logsfile:
            today = datetime.now()
            logsfile.write(f"{today}: File encrypted: {filepath}\n")
    except Exception as e:
        with open('logs_client.txt', "a") as logsfile:
            today = datetime.now()
            logsfile.write(f"{today}: Encryption failure: {e}\n")


def decrypt(connection: socket, filepath):  # Decrypt and verify file
    connection.sendall(filepath.encode('utf-8'))  # Send file path to server
    print("Decrypting and verify sign")
    try:
        with open(filepath, "rb") as file:
            while True:
                data = file.read(SIZE_BUFF)
                if not data:
                    break
                connection.sendall(data)  # Send encrypted file to server
        with open('logs_client.txt', "a") as logsfile:  # Write log
            today = datetime.now()
            logsfile.write(f"{today}: Decrypt file: {filepath}\n")
    except Exception as e:
        with open('logs_client.txt', "a") as logsfile:
            today = datetime.now()
            logsfile.write(f"{today}: Decrytion failure: {e}\n")


def fileExplorer(wildcard):  # Open a window to select a file
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path


main()
