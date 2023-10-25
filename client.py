import socket
import argparse
import threading
import sys
import datetime


def join_chatroom(host, port, username, passcode):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send info to the server
    client_socket.send(f"{username}:{passcode}".encode())

    # Wait for server response
    response = client_socket.recv(1024).decode()
    print(response)
    sys.stdout.flush()

    if response != "Incorrect passcode":
        # Start a thread for receiving messages from the server
        receive_thread = threading.Thread(
            target=receive_messages, args=(client_socket, username)
        )
        receive_thread.start()

        # Handle user input in the main thread
        handle_user_input(username, client_socket)


# To show texts from one client to another
def receive_messages(client_socket, username):
    while True:
        message = client_socket.recv(1024).decode()
        if message:
            print(message)
            sys.stdout.flush()
        if message == ":Exit":
            break


# Input client side messages and handle them
def handle_user_input(username, client_socket):
    while True:
        message = input()

        # Check for special commands
        if message == ":)":
            message = "[feeling happy]"
        elif message == ":(":
            message = "[feeling sad]"
        elif message == ":mytime":
            current_time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
            message = current_time
        elif message == ":+1hr":
            current_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            formatted_time = current_time.strftime("%a %b %d %H:%M:%S %Y")
            message = formatted_time

        client_socket.send(message.encode())

        if message == ":Exit":
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat Room Client")
    parser.add_argument(
        "-join", action="store_true", help="Starts the server", required=False
    )
    parser.add_argument("-host", type=str, help="Server's IP address", required=True)
    parser.add_argument("-port", type=int, help="Server's port number", required=True)
    parser.add_argument("-username", type=str, help="Your username", required=True)
    parser.add_argument(
        "-passcode", type=str, help="Password to connect to the chatroom", required=True
    )
    args = parser.parse_args()

    join_chatroom(args.host, args.port, args.username, args.passcode)
