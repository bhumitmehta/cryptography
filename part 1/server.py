# server.py - Bob's side in a Diffie-Hellman key exchange with Alice

import socket
import random

# Diffie-Hellman parameters
PRIME_MOD = 23
BASE = 5

# Generate private and public keys
bob_private_key = random.randint(1, PRIME_MOD - 1)
bob_public_key = pow(BASE, bob_private_key, PRIME_MOD)

# Simple XOR-based encryption function
def encrypt_decrypt_message(message, key):
    return ''.join(chr(ord(char) ^ key) for char in message)

# Setup server to connect with Alice
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(1)
print("Bob (server) is waiting for Alice to connect...")

# Accept connection from Alice
connection, address = server.accept()
print("Connected by", address)

# Receive Alice's public key
alice_public_key = int(connection.recv(1024).decode())
print(f"Alice's public key received: {alice_public_key}")

# Send Bob's public key to Alice
connection.sendall(str(bob_public_key).encode())
print(f"Bob's public key sent to Alice: {bob_public_key}")

# Calculate the shared key
shared_key = pow(alice_public_key, bob_private_key, PRIME_MOD)
print(f"Shared key with Alice: {shared_key}")

# Receive encrypted message from Alice
encrypted_message = connection.recv(1024).decode()
decrypted_message = encrypt_decrypt_message(encrypted_message, shared_key)
print(f"Decrypted message from Alice: {decrypted_message}")

# Send a response back to Alice
response = "Hello, Alice!"
encrypted_response = encrypt_decrypt_message(response, shared_key)
connection.sendall(encrypted_response.encode())
print(f"Encrypted response sent to Alice: {encrypted_response}")

# Keep the server open
input("Press Enter to close the server...")

# Close the connection
connection.close()
server.close()
