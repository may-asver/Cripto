"""
    Script that allows to user:
    1. Login
    2. Select a file
    3. Encrypt and sign a file
    4. Decrypt and verify file's sign
    7. File to save logs

    Author: Maya Aguirre
    Date: May, 11 2022
"""
from argon2 import PasswordHasher as hasher


def login_menu():  # Login menu
    print("Log in")
    user = input("user> ")
    psswd = input("password> ")
    if user == "" or psswd == "":
        print("User or password is empty. Try again.")
        login_menu()
    else:
        pswd_hash = hasher().hash(psswd)
        return user, pswd_hash


def menu_operations():  # Menu operations
    # Show options
    print("1. Encrypt file")
    print("2. Decrypt file")
    print("0. Exit")
    operation = int(input("?> "))
    if operation < 0 or operation > 2:
        print("Bad operation. Try again.")
        menu_operations()
    else:
        return operation
