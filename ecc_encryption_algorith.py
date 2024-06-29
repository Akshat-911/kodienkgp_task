from ecdsa import SigningKey, SECP256k1, ellipticcurve
from ecdsa.ellipticcurve import Point
import hashlib
import os

# Helper function to generate a random integer in the range [1, n-1]
def random_integer(order):
    return int.from_bytes(os.urandom(32), byteorder='big') % order # modulo by order to keep the integer within the range

# Key Generation
def generate_keys():
    private_key = random_integer(SECP256k1.order) ##SECP256K1 is a specific elliptic curve used in cryptograpghy.
    public_key = private_key * SECP256k1.generator ## multiplying the private key with the base point
    return private_key, public_key


def msg_to_point(message, curve): # converts the plaintext to points on the curve.
    message_hash = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big')
    while True: #rubn a loop till we find the a valid point
        x = message_hash % curve.p() #modulu by curve.p()so that it remains on the prime field defined.
        y_square = (x**3 + curve.a() * x + curve.b()) % curve.p()
        y = pow(y_square, (curve.p() + 1) // 4, curve.p())
        if (y * y) % curve.p() == y_square: #checking if its valid.
            return Point(curve, x, y)
        message_hash += 1

# Decoding point to message
def point_to_msg(point, curve):
    message_hash = point.x() 
    while True:
        candidate_hash = hashlib.sha256(message_hash.to_bytes( byteorder='big')).digest() # the msg(integer) is converted into bytes and then finally to hash
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

# Example
private_key, public_key = generate_keys()
print("Private Key:", private_key)
print("Public Key:", (public_key.x(), public_key.y()))

# Example msg
plaintext_message = b"Hello, World!"

# Encrypt the message
ciphertext = encrypt_message(public_key, plaintext_message)
print("Ciphertext:", ((ciphertext[0].x(), ciphertext[0].y()), (ciphertext[1].x(), ciphertext[1].y())))

# Decrypt the message
decrypted_message = decrypt_message(private_key, ciphertext)
print("Decrypted Message:", decrypted_message.decode())
