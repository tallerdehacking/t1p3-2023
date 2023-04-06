import os
import socket
import threading
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from .const import *

flag = os.getenv("FLAG", "Q0M1MzJYLXRyeSBoYXJkZXItCg==")
pk = serialization.load_pem_public_key(os.getenv("PUBLIC_KEY", ""),password=None)


def handle(c):
    c.sendall(b"Adjunta un mensaje de 5326 tal cual como lo recibiste y contestare tu pregunta.\n\n")
    try:
        received = json.loads(c.recv(4096).decode().strip())
        message_to_int = int.from_bytes(bytes.fromhex(received.get("message", "")), byteorder='big')
        if received.get("signature", "") == pow(message_to_int, pk.public_numbers.e, pk.public_numbers.n):
            if received.get("message") == FORBIDDEN_QUESTION.hex():
                s.sendall(b"Felicidades!\n\n\nLa flag es" + flag.encode() + b"\n\n")
            else:
                s.sendall(random.choice(PREDICTIONS).encode() + b"\n\n")
    except Exception as e:
        print(e) 
        c.sendall(b"No entendi. Adiós!\n")
        c.close()

if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", 5327))
        s.listen()

        while True:
            c, _ = s.accept()
            # Send each "client_soc" connection as a parameter to a thread.
            threading.Thread(target=handle,args=(c,), daemon=True).start()
    except KeyboardInterrupt:
        print("Closing socket...")
        s.close()