from ecdsa import SigningKey, SECP256k1, ellipticcurve
from ecdsa.ellipticcurve import Point
import hashlib
import os
import socket
import threading

# Helper function to generate a random integer in the range
def random_integer(order):
    return int.from_bytes(os.urandom(32), byteorder='big') % order #modulo so that it doestn go out of bounds

# Key Generation
def generate_keys():
    private_key = random_integer(SECP256k1.order) #SECP256K1 is a specific elliptic curve used in cryptography
    public_key = private_key * SECP256k1.generator #.generator generates the base point.
    return private_key, public_key

def msg_to_point(message, curve):
    message_hash = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big') 
    while 1:
        x = message_hash % curve.p()
        y_square = (x**3 + curve.a() * x + curve.b()) % curve.p()
        y = pow(y_square, (curve.p() + 1) // 4, curve.p())
        if (y * y) % curve.p() == y_square: #checking if valid
            return Point(curve, x, y)
        message_hash += 1

# Decoding point to message
def point_to_msg(point, curve):
    message_hash = point.x()
    while 1:
        candidate_hash = hashlib.sha256(message_hash.to_bytes( byteorder='big')).digest() #first convert the msg hash(int) to a byte sequence and then to a hash
        x = int.from_bytes(candidate_hash, byteorder='big') % curve.p()
        if x == point.x():
            return candidate_hash
        message_hash -= 1

# Encryption
def encrypt_message(public_key, plaintext_message):
    curve = SECP256k1.curve
    base_point = SECP256k1.generator
    k = random_integer(SECP256k1.order)
    kG = k * base_point
    kQ = k * public_key
    Pm = msg_to_point(plaintext_message, curve)
    cipher_text = (kG, Pm + kQ)
    return cipher_text

# Decryption
def decrypt_message(private_key, cipehr_text):
    kG, Pm_kQ = cipehr_text
    kQ = private_key * kG
    decrypted_point = Pm_kQ - kQ
    curve = SECP256k1.curve
    return point_to_msg(decrypted_point, curve)

clients = []
client_names = {}

def send_msg(msg, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(msg)

def chat_with_client(client_socket):
    name = client_socket.recv(1024).decode('ascii')
    client_names[client_socket] = name
    intro_msg = f"{name} has joined the chat!".encode('ascii')
    send_msg(intro_msg, client_socket)
    print(intro_msg.decode('ascii'))

    while True:
        msg = client_socket.recv(1024)
        if msg:
            # Decrypt message
            decrypted_msg = decrypt_message(private_key, eval(msg.decode('ascii')))  # Assuming msg is evaluable to cipehr_text
            msg_to_send = f"{name}: {decrypted_msg.decode('ascii')}".encode('ascii')
            print(msg_to_send.decode('ascii'))
            send_msg(msg_to_send, client_socket)
        else:
            clients.remove(client_socket)
            client_socket.close()
            leaving_msg = f"{name} has left the chat.".encode('ascii')
            send_msg(leaving_msg, client_socket)
            print(leaving_msg.decode('ascii'))
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)
    print("Server started, waiting for connections....")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        clients.append(client_socket)
        threading.Thread(target=chat_with_client, args=(client_socket,)).start()

start_server()
