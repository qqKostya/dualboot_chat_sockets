import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

clients = set()


def new_client(connection: socket.socket, address: tuple) -> None:
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break

            with open("logs.txt", "a") as f:
                f.write(
                    f"Received message '{data.decode()}' from {address[0]}:{address[1]}\n"
                )

            for client in clients:
                if client is not connection:
                    client.sendall(data)

    clients.remove(connection)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print(f"New client connected: {addr}")

        clients.add(conn)

        client_thread = threading.Thread(target=new_client, args=(conn, addr))
        client_thread.start()
