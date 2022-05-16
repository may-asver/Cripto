# How it works

TCP server and client to receive/send files.
User can select a file from the file explorer pop-up, then the client encrypts and sign the file, server receive th file and saves it.
To decryp the file and verify sign, user selects it from file explorer pop-up.

Client and server save their logs for admin reasons.


# Libraries
Python libraries used for tcp_client.py and tcp_server.py:

- wxPython310
- dotenv
- argon2
