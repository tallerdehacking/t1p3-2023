import os
import socket
import threading
import random
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from .const import *



sk = serialization.load_pem_private_key(os.getenv("PRIVATE_KEY", ""),password=None)


def handle(c):
    c.sendall(
        b"Preguntame lo que quieras en hexadecimal (menos \"" + \n
        FORBIDDEN_QUESTION + \
        "\") y te lo contestare.\n\n"
    )
    try:
        received = c.recv(1024).decode().strip()
        if received.strip() == FORBIDDEN_QUESTION.hex():
            s.sendall(random.choice(FORBIDDEN_ANSWERS).encode())
        else:
            message_to_int = int.from_bytes(bytes.fromhex(received), byteorder='big')
            answer = {
                "message": received
                "signature": pow(message_to_int, sk.private_numbers.d, sk.private_numbers.public_numbers.n)
            }
            s.sendall(json.dumps(answer))
    except Exception as e:
        print(e) 
        c.sendall(b"No entendi. Adiós!\n")
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