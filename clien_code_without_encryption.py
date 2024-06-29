import socket
import threading
#client code
def receive_msg(client_socket):  #receive msgs from the server and prints them
    while True:
        try:
            msg = client_socket.recv(1024).decode('ascii') #receives the msgs and decodes them into strings
            if msg:  #prints the msg if not empty
                print(msg)
        except:
            print("An error occurred.")
            client_socket.close()  #terminates the connection of the client if msg is empty
            break

def send_messages(client_socket):
    while True:
        message = input('')
        to_send=message.encode('ascii');
        client_socket.send(to_send)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345)) ##connecting to tthe server
    
    name = input("Enter your name: ")
    send_name=name.encode('ascii');
    client_socket.send(send_name)
    
    thread_rcv = threading.Thread(target=receive_msg, args=(client_socket,))
    thread_rcv.start()
    
    thread_send = threading.Thread(target=send_messages, args=(client_socket,))
    thread_send.start()


 main()
