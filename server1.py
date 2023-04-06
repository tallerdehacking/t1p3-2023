import os
import socket
import threading
import random
import json
from cryptography.hazmat.primitives import serialization
from const import *



sk = serialization.load_pem_private_key(os.getenv("PRIVATE_KEY", "").encode(),password=None)
d = sk.private_numbers().d
n = sk.private_numbers().public_numbers.n

def handle(c):
    c.sendall(
        b"Preguntame lo que quieras en hexadecimal (menos \"" + \
        FORBIDDEN_QUESTION.encode() + \
        b"\") y te lo contestare.\n\n"
    )
    try:
        received = c.recv(1024).decode().strip()
        message_to_int = int.from_bytes(bytes.fromhex(received), byteorder='little')
        print("message to int is", message_to_int)
        if received.strip() == FORBIDDEN_QUESTION.encode().hex():
            c.sendall(random.choice(FORBIDDEN_ANSWERS).encode() + b"\n\n")
        else:
            answer = {
                "message": received,
                "signature": pow(message_to_int, d, n)
            }
            c.sendall(json.dumps(answer).encode() + b"\n\n")
    except Exception as exception:
        print(exception) 
        c.sendall(b"No entendi.\n")
    c.sendall(b"Adios!\n\n")
    c.close()

if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", 5326))
        s.listen()

        while True:
            c, _ = s.accept()
            # Send each "client_soc" connection as a parameter to a thread.
            threading.Thread(target=handle,args=(c,), daemon=True).start()
    except KeyboardInterrupt:
        print("Closing socket...")
        s.close()