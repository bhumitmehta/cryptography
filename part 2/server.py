import socket
import random

def diffie_hellman(p, g, b):
    B = pow(g, b, p)
    return B

def server():
    p = 23  
    g = 5   
    b = random.randint(2, p-2)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 65432)
    sock.bind(server_address)

    sock.listen(1)
    print('Bob is waiting for a connection from Alice...')
    connection, client_address = sock.accept()

    try:
        print(f"p={p}, g={g}")
        connection.sendall(f'{p},{g}'.encode())

        # Receive A from Alice
        A = int(connection.recv(1024).decode())
        print("A from Alice:", A)
        
        # Send B to Alice
        B = diffie_hellman(p, g, b)
        connection.sendall(str(B).encode())
        print("B to Alice:", B)

        # Calculate shared secret
        shared_secret_B = pow(A, b, p)
        print(f"Bob's shared secret: {shared_secret_B}")

        # Receive a message from Alice and reply
        message_from_alice = connection.recv(1024).decode()
        print("Message from Alice:", message_from_alice)
        
        # Bob sends a response
        message=input("Enter message to send:")
        connection.sendall(message.encode())

    finally:
        connection.close()

if __name__ == '__main__':
    server()
