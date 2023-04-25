import socket
import logging
from threading import Thread
from datetime import datetime
from typing import Set

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

logging.basicConfig(level=logging.INFO)
client_sockets: Set[socket.socket] = set()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen()
logging.info(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

date_now = datetime.now().strftime("%m/%d %H:%M:%S")


def send_message(message: bytes, current_socket: socket.socket) -> None:
    for client in client_sockets:
        if not client == current_socket:
            client.sendall(message)


def listen_for_client(client: socket.socket) -> None:
    client_addr = client.getpeername()
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                raise socket.error
        except socket.error as e:
            client_sockets.remove(client)
            client.close()
            logging.info(f"[-] {date_now} {client_addr} disconnected. \n{e}")
            break
        else:
            logging.info(f"{client_addr} - {msg.decode()}")
            send_message(msg, client)


while True:
    client_socket, client_address = s.accept()
    logging.info(f"[+] {date_now} {client_address} connected.")
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()
