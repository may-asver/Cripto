"""
    Script to print random hex numbers with PyNaCl
    Author: Maya Aguirre
    Date: 05/04/2022
"""

import nacl.utils
import nacl.secret


def random_Number(size):
    return nacl.utils.random(size)


def main():
    number = random_Number(32)
    print(number.hex())


def menu():
    print("Generar números pseudoaleatorios hexadecimales de 256 bits con PyNaCl")
    print("1. Iniciar\n0. Salir")
    option = int(input("> "))
    if option:
        main()
        return 1
    else:
        return 0


go_out = 1
while go_out:
    go_out = menu()
