import socket
import threading

clients = []
client_names = {} # dictionary to store the names of the clients

def send_msg(msg, client_socket):
    for i in clients:
        if i != client_socket:
                i.send(msg)

def chat_with_client(client_socket):
        # Receive and store clients name
        name = client_socket.recv(1024).decode('ascii')
        client_names[client_socket] = name
        intro_msg = f"{name} has joined the chat!".encode('ascii')
        send_msg(intro_msg, client_socket)
        print(intro_msg.decode('ascii')) #displays the msg sent to all the clients.

        while True:
            msg = client_socket.recv(1024)
            if msg:
                msg_to_send = f"{name}: {msg.decode('ascii')}".encode('ascii') #formatted msg(which is encoded to bytes) to include the name of the sender
                print(msg_to_send.decode('ascii')) # displays the decoded msg on the server console.
                send_msg(msg_to_send, client_socket)
            else:  #if msg is empty then remove the client from the list and terminates its connection.
                clients.remove(client_socket)
                client_socket.close()
                leaving_msg = f"{name} has left the chat.".encode('ascii')
                send_msg(leaving_msg, client_socket)
                print(leaving_msg.decode('ascii'))
                break
            
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #creating a socket of internet type and TCP protocol
    server.bind(('localhost', 12345))
    server.listen(5) #listening mode
    print("Server started, waiting for connections....")

    while 1:
        client_socket, adr = server.accept()
        print(f"Connection from {adr}")
        clients.append(client_socket)
        new_thread = threading.Thread(target=chat_with_client, args=(client_socket,)) ## creates a new thread fpr each client to handle multiple clients concurrently
        new_thread.start()

    start_server()
