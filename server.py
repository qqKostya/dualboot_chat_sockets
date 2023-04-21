import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 12345

clients = set()


def new_client(connection: socket.socket) -> None:
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print(f"Received {data}")

            for client in clients:
                if client is not connection:
                    connection.sendall(b"Hello client")

    clients.remove(connection)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, _ = s.accept()
        clients.add(conn)
        client_thread = Thread(target=new_client, args=(conn,))
        client_thread.start()
