import socket
import threading

# Set up a socket for listening on a specific port
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('localhost', 9999))
listen_socket.listen()


# Define a function for handling incoming connections
def handle_connection(client_socket):
    # Receive data from the client
    request_data = client_socket.recv(1024)

    # Process the request
    response_data = b"Hello, world!"

    # Send the response back to the client
    client_socket.sendall(response_data)

    # Close the socket
    client_socket.close()


# Define a function for accepting incoming connections
def accept_connections():
    while True:
        # Accept a new connection
        client_socket, client_address = listen_socket.accept()

        # Spawn a new thread to handle the connection
        client_thread = threading.Thread(target=handle_connection, args=(client_socket,))
        client_thread.start()


# Start accepting incoming connections in a separate thread
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Connect to another peer
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer_socket.connect(('localhost', 9999))

# Send a message to the other peer
peer_socket.sendall(b"Hello from the other peer!")

# Receive a response from the other peer
response_data = peer_socket.recv(1024)
print(response_data)

# Close the peer socket
peer_socket.close()
