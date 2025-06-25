# 🔐 ECC Encrypted Client-Server Chat Application

A Python-based client-server messaging application that supports both **unencrypted** and **Elliptic Curve Cryptography (ECC) encrypted** communication. This project demonstrates the integration of ECC for secure real-time data transmission between clients and a server.

## 📂 Project Structure

```
.
├── client_code_with_encryption.py       # Encrypted client implementation
├── server_code_with_encryption.py       # Encrypted server implementation
├── ecc_encryption_algorithm.py          # ECC key generation, encryption, decryption logic
├── clien_code_without_encryption.py     # Basic unencrypted client (typo in filename)
├── server_code_without_encryption.py    # Basic unencrypted server
```

## 🔧 Requirements

- Python 3.x
- `ecdsa` library for ECC operations  
  Install using:
  ```bash
  pip install ecdsa
  ```

## 🔐 Features

- ✅ **Encrypted Communication**: Uses ECC for secure messaging
- ✅ **Asymmetric Key Exchange**: ECC public-private key pair generation
- ✅ **Digital Signatures**: Ensures message integrity and authenticity
- ✅ **Unencrypted Versions Included**: For comparison or testing basic socket communication
- ✅ **Threaded Client Handling**: Server can handle multiple clients concurrently

## 🚀 How to Run

### 🔸 1. Unencrypted Version

Start the server:
```bash
python server_code_without_encryption.py
```

Start the client (in a new terminal):
```bash
python clien_code_without_encryption.py
```

### 🔸 2. Encrypted Version

Start the encrypted server:
```bash
python server_code_with_encryption.py
```

Start the encrypted client:
```bash
python client_code_with_encryption.py
```

## 🔐 ECC Module (`ecc_encryption_algorithm.py`)

This module handles:
- ECC key pair generation
- Message encryption using the public key
- Message decryption using the private key
- Optional signing and verification for secure message authenticity

## 💡 Example ECC Workflow

1. Both client and server generate their ECC key pairs.
2. They exchange public keys on connection.
3. Messages are encrypted using the recipient's public key and decrypted using the sender's private key.

## ⚠️ Note

- File `clien_code_without_encryption.py` appears to have a **typo** (`clien` → `client`). Consider renaming it for clarity.
- The ECC implementation here is simplified for learning purposes. For production use, rely on well-vetted cryptographic libraries and secure protocols like TLS.

## 📚 References

- [Elliptic Curve Cryptography (Wikipedia)](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography)
- [Python `ecdsa` Library Documentation](https://pypi.org/project/ecdsa/)
- Python's built-in `socket`, `threading`, and `hashlib` modules

## 📜 License

This project is licensed under the MIT License. See `LICENSE` file for details.
