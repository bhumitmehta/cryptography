import socket
import random

def diffie_hellman(p, g, e):
    E = pow(g, e, p)
    return E

def mitm():
    sock_to_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_to_alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address_bob = ('localhost', 65432)
    server_address_alice = ('localhost', 65433)
    
    sock_to_bob.connect(server_address_bob)
    sock_to_alice.bind(server_address_alice)
    sock_to_alice.listen(1)
    print('Eve is waiting for a connection from Alice...')
    connection, client_address = sock_to_alice.accept()

    try:
        # Intercept and relay Diffie-Hellman parameters
        data = sock_to_bob.recv(1024).decode()
        connection.sendall(data.encode())
        p, g = map(int, data.split(','))
        print(f"p={p}, g={g} from Server")
        e = random.randint(2, p-2)

        # Intercept A from Alice and relay to Bob
        A = int(connection.recv(1024).decode())
        print("A intercepted from Alice:", A)
        E_to_B = diffie_hellman(p, g, e)
        sock_to_bob.sendall(str(E_to_B).encode())
        print("Key shared to Bob from Eve:", E_to_B)

        # Intercept B from Bob and relay to Alice
        B = int(sock_to_bob.recv(1024).decode())
        print("B intercepted from Bob:", B)
        E_to_A = diffie_hellman(p, g, e)
        connection.sendall(str(E_to_A).encode())
        print("Key shared to Alice from Eve:", E_to_A)

        # Calculate shared secrets
        shared_secret_with_alice = pow(A, e, p)
        shared_secret_with_bob = pow(B, e, p)
        print(f"Eve's shared secret with Alice: {shared_secret_with_alice}")
        print(f"Eve's shared secret with Bob: {shared_secret_with_bob}")

        # Intercept message from Alice and relay it to Bob
        message_from_alice = connection.recv(1024).decode()
        print("Message intercepted from Alice:", message_from_alice)
        message_to_bob=input("Enter changed message:")
        print("This is sent to BOB:"+message_to_bob)
        sock_to_bob.sendall(message_to_bob.encode())

        # Intercept message from Bob and relay it to Alice
        message_from_bob = sock_to_bob.recv(1024).decode()
        print("Message intercepted from Bob:", message_from_bob)
        message_to_alice=input("Enter changed message:")
        print("This is sent to ALICE:"+message_to_alice)
        connection.sendall(message_to_alice.encode())

    finally:
        sock_to_bob.close()
        sock_to_alice.close()

if __name__ == '__main__':
    mitm()


