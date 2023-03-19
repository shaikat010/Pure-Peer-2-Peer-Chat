import socket
import threading

HOST = '127.0.0.1'
PEER_PORT = int(input("Give me the Port to Connect to: "))
nickname = input("Choose your nickname before joining server: ")

# defining a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 55555
client.bind((HOST,PORT))

client.listen()

def connect():
    # this is the ip of the server that we want to connect to
    client.connect(('127.0.0.1', PEER_PORT))


def receive():
    # always tries to receive data from the server
    while True:
        try:
            # receiving from the server
            message = client.recv(1024).decode('ascii')
            print(message)

        except:
            (print("An error occured!"))
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))



connect()

# we are running 2 threads receive thread and the write thread

# the thread for receiving
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# the thread for writing
write_thread = threading.Thread(target=write)
write_thread.start()

