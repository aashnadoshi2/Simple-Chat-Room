import socket
import argparse
import sys
import threading


def start_server(port, passcode):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    print(f"Server started on port {port}. Accepting connections")
    sys.stdout.flush()

    clients = (
        {}
    )  # Dictionary to store connected clients (client username: client socket)

    # Handles messages for a single client

    while True:
        client_socket, client_address = server_socket.accept()

        # Continuously check for info from client
        username, password = client_socket.recv(1024).decode().split(":")
        if password == passcode:
            clients[username] = client_socket
            print(f"{username} joined the chatroom")
            sys.stdout.flush()

            broadcast(f"{username} joined the chatroom", clients, username)
            connected_message = f"Connected to {client_address[0]} on port {port}"
            client_socket.send(connected_message.encode())

            # Create a new thread for the client and call the handle_client function
            client_thread = threading.Thread(
                target=handle_client, args=(username, client_socket, clients)
            )
            client_thread.start()
        else:
            client_socket.send("Incorrect passcode".encode())
            client_socket.close()


def broadcast(message, clients, sender=None):
    for username, client_socket in clients.items():
        if username != sender:
            client_socket.send(message.encode())


def handle_client(username, client_socket, clients):
    # Handles messages for a client
    while True:
        message = client_socket.recv(1024).decode()
        if message == ":Exit":
            client_socket.close()
            del clients[username]
            print(f"{username} left the chatroom")
            sys.stdout.flush()
            broadcast(f"{username} left the chatroom", clients)
            break

        # If message is not empty, we broadcast
        elif message.strip():
            print(f"{username}: {message}")
            sys.stdout.flush()
            broadcast(f"{username}: {message}", clients, sender=username)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat Room Server")
    parser.add_argument(
        "-start", action="store_true", help="Starts the server", required=False
    )
    parser.add_argument(
        "-port", type=int, help="Port number to listen on", required=True
    )
    parser.add_argument(
        "-passcode", type=str, help="Password for clients to connect", required=True
    )
    args = parser.parse_args()

    start_server(args.port, args.passcode)
