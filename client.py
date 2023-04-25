import socket
import threading
from datetime import datetime

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
print(f"[+] Connected to {SERVER_HOST}:{SERVER_PORT}. Type 'q' for exit")
name = input("Enter your name: ")


def listen_for_messages() -> None:
    while True:
        try:
            message = s.recv(1024)
            if not message:
                raise socket.error
        except socket.error as err:
            print(f"[!] Error: {err}")
            s.close()
            break
        else:
            message_str = message.decode()
            print(f"\n {message_str}")


t = threading.Thread(target=listen_for_messages, daemon=True)
t.start()

while True:
    to_send = input()
    if to_send.lower() == "q":
        break
    date_now = datetime.now().strftime("%m/%d %H:%M:%S")
    to_send = f"({date_now}) {name}: {to_send}"
    try:
        s.sendall(to_send.encode())
    except OSError as e:
        print(f"[!] Error: {e}")
        break

s.close()
