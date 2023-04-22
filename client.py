import socket
import threading

HOST = "127.0.0.1"
PORT = 12345


def send_messages(sock: socket.socket, client_name: str) -> None:
    while True:
        message = input()
        if message == "/quit":
            sock.close()
            return
        message_with_name = f"{client_name}: {message}"
        sock.sendall(message_with_name.encode())


def recv_messages(sock: socket.socket) -> None:
    while True:
        data = sock.recv(1024)
        if not data:
            print("Disconnected from server")
            return
        print(f"Received {data.decode()}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    print('To close the chat, enter "quit"')
    client_name = input("Enter your name: ")

    send_thread = threading.Thread(target=send_messages, args=(s, client_name))
    recv_thread = threading.Thread(target=recv_messages, args=(s,))

    send_thread.start()
    recv_thread.start()

    send_thread.join()
    recv_thread.join()
