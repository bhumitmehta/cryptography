import socket
import random

def diffie_hellman(p, g, a):
    A = pow(g, a, p)
    return A

def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 65433)
    sock.connect(server_address)

    try:
        # Receive Diffie-Hellman parameters
        data = sock.recv(1024).decode()
        p, g = map(int, data.split(','))
        print(f"p={p}, g={g}")
        a = random.randint(2, p-2)

        # Send A to Bob
        A = diffie_hellman(p, g, a)
        sock.sendall(str(A).encode())
        print("A to Bob:", A)

        # Receive B from Bob
        B = int(sock.recv(1024).decode())
        print("B from Bob:", B)

        # Calculate shared secret
        shared_secret_A = pow(B, a, p)
        print(f"Alice's shared secret: {shared_secret_A}")

        # Send a message to Bob
        message=input("Enter a message to send:")
        sock.sendall(message.encode())

        # Receive a response from Bob
        message_from_bob = sock.recv(1024).decode()
        print("Message from Bob:", message_from_bob)

    finally:
        sock.close()

if __name__ == '__main__':
    client()

