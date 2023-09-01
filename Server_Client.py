import socket
import threading



def receive_message(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print("Recebido:",data.decode())

HOST = '127.0.0.1'
PORT = 443

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Aguardando conexão...")
    client_socket, client_address = server_socket.accept()
    print("Conexão estabelecida com:", client_address)
    
    receive_message()





    client_socket.close()
    server_socket.close()



def start_client():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("Conexão com o servidor estabelecida.")
    client_socket.close()





