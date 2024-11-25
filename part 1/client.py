# client.py - Alice's side in a Diffie-Hellman key exchange with Bob

import socket
import random

# Diffie-Hellman parameters
PRIME_MOD = 23
BASE = 5

# Generate private and public keys
alice_private_key = random.randint(1, PRIME_MOD - 1)
alice_public_key = pow(BASE, alice_private_key, PRIME_MOD)

# Simple XOR-based encryption function
def encrypt_decrypt_message(message, key):
    return ''.join(chr(ord(char) ^ key) for char in message)

# Connect to Bob (server)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))
print("Alice (client) connected to Bob.")

# Send Alice's public key to Bob
client.sendall(str(alice_public_key).encode())
print(f"Alice's public key sent: {alice_public_key}")

# Receive Bob's public key
bob_public_key = int(client.recv(1024).decode())
print(f"Bob's public key received: {bob_public_key}")

# Calculate the shared key
shared_key = pow(bob_public_key, alice_private_key, PRIME_MOD)
print(f"Shared key with Bob: {shared_key}")

# Encrypt and send a message to Bob
message = "Hello, Bob!"
encrypted_message = encrypt_decrypt_message(message, shared_key)
client.sendall(encrypted_message.encode())
print(f"Encrypted message sent to Bob: {encrypted_message}")

# Receive and decrypt response from Bob
encrypted_response = client.recv(1024).decode()
decrypted_response = encrypt_decrypt_message(encrypted_response, shared_key)
print(f"Decrypted response from Bob: {decrypted_response}")

# Keep the client open
input("Press Enter to close the client...")

# Close the connection
client.close()
