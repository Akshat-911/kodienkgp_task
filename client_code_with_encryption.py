from ecdsa import SigningKey, SECP256k1, ellipticcurve
from ecdsa.ellipticcurve import Point
import hashlib
import os
import socket
import threading

# Helper function to generate a random integer in the range [1, n-1]
def random_integer(order):
    return int.from_bytes(os.urandom(32), byteorder='big') % order

# Key Generation
def generate_keys():
    private_key = random_integer(SECP256k1.order)
    public_key = private_key * SECP256k1.generator
    return private_key, public_key

def msg_to_point(message, curve):
    message_hash = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big')
    while True:
        x = message_hash % curve.p()
        y_square = (x**3 + curve.a() * x + curve.b()) % curve.p()
        y = pow(y_square, (curve.p() + 1) // 4, curve.p())
        if (y * y) % curve.p() == y_square:
            return Point(curve, x, y)
        message_hash += 1

# Decoding point to message
def point_to_msg(point, curve):
    message_hash = point.x()
    while True:
        candidate_hash = hashlib.sha256(message_hash.to_bytes( byteorder='big')).digest()
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
    ciphertext = (kG, Pm + kQ)
    return ciphertext

# Decryption
def decrypt_message(private_key, ciphertext):
    kG, Pm_kQ = ciphertext
    kQ = private_key * kG
    decrypted_point = Pm_kQ - kQ
    curve = SECP256k1.curve
    return point_to_msg(decrypted_point, curve)

def send_messages(client_socket):
    while True:
        message = input('')
        encrypted_message = encrypt_message(public_key, message.encode('ascii'))
        client_socket.send(str((encrypted_message[0].x(), encrypted_message[0].y()), (encrypted_message[1].x(), encrypted_message[1].y())).encode('ascii'))

def receive_msg(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('ascii')
            if msg:
                decrypted_msg = decrypt_message(private_key, eval(msg))
                print(decrypted_msg.decode('ascii'))
        except:
            print("An error occurred.")
            client_socket.close()
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client_socket.connect(('localhost', 12345))
    
    name = input("Enter your name: ")
    client_socket.send(name.encode('ascii'))
    
    thread_rcv = threading.Thread(target=receive_msg, args=(client_socket,))
    thread_rcv.start()
    
    thread_send = threading.Thread(target=send_messages, args=(client_socket,))
    thread_send.start()

main()
