import socket
import threading

# Set up a socket for listening on a specific port
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('localhost', 9999))
listen_socket.listen()


# Define a function for handling incoming connections
def handle_connection(client_socket, client_address):
    while True:
        # Receive data from the client
        request_data = client_socket.recv(1024)

        # Check if the client has disconnected
        if not request_data:
            print(f"{client_address} has disconnected")
            break

        # Print the message from the client
        message = request_data.decode()
        print(f"{client_address}: {message}")

        # Send the message to all other connected clients
        for peer_socket in peer_sockets:
            if peer_socket != client_socket and peer_socket not in sent_sockets:
                peer_socket.sendall(request_data)
                sent_sockets.append(peer_socket)

    # Close the socket
    client_socket.close()


# Define a function for accepting incoming connections
def accept_connections():
    while True:
        # Accept a new connection
        client_socket, client_address = listen_socket.accept()
        print(f"{client_address} has connected")

        # Add the client socket to the list of peer sockets
        peer_sockets.append(client_socket)

        # Spawn a new thread to handle the connection
        client_thread = threading.Thread(target=handle_connection, args=(client_socket, client_address))
        client_thread.start()


# Start accepting incoming connections in a separate thread
peer_sockets = []
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Connect to other peers
while True:
    peer_address = input("Enter the IP address of a peer to connect to (or press Enter to stop): ")
    if not peer_address:
        break

    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.connect((peer_address, 9999))
    peer_sockets.append(peer_socket)


    # Spawn a new thread to receive messages from the peer
    def handle_peer(peer_socket):
        while True:
            # Receive data from the peer
            request_data = peer_socket.recv(1024)

            # Check if the peer has disconnected
            if not request_data:
                print(f"{peer_socket.getpeername()} has disconnected")
                peer_sockets.remove(peer_socket)
                break

            # Print the message from the peer
            message = request_data.decode()
            print(f"{peer_socket.getpeername()}: {message}")


    peer_thread = threading.Thread(target=handle_peer, args=(peer_socket,))
    peer_thread.start()

# Send messages to other peers
while True:
    message = input("Enter a message to send to other peers (or press Enter to quit): ")
    if not message:
        break

    message_data = message.encode()
    sent_sockets = []

    for peer_socket in peer_sockets:
        if peer_socket not in sent_sockets:
            peer_socket.sendall(message_data)
            sent_sockets.append(peer_socket)

# Close all sockets
listen_socket.close()
for peer_socket in peer_sockets:
    peer_socket.close()
