import socket, tqdm, os
from funcoes import aguarde

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

host = "127.0.0.1"
port = 443

def send_public_key(filename, sonda_nome):
    try:
        filesize = os.path.getsize(filename)
    except:
        print("Arquivo não encontrado!")
        return
    
    tcp_socket = socket.socket()
    tcp_socket.connect((host, port))
    print(f"Conectado com {host}:{port}")

    aguarde(1)

    tcp_socket.sendall(sonda_nome.encode())
    aguarde(0.5)

    file_type = "publickey"

    tcp_socket.sendall(file_type.encode())

    data_to_send = f"{file_type}{SEPARATOR}{filename}{SEPARATOR}{filesize}"
    aguarde(1)
    
    tcp_socket.send(data_to_send.encode())

    progress = tqdm.tqdm(range(filesize), f"Enviando: {filename}", unit="B", unit_scale=True, unit_divisor=256)
    with open(filename, "rb") as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                break       
            tcp_socket.sendall(bytes_read)
            progress.update(len(bytes_read))
    
    tcp_socket.close()
    os.remove(filename)


def send_arquivs(filename, sonda_nome ,file_type):
    try:
        filesize = os.path.getsize(filename)
    except:
        print("Arquivo não encontrado!")
        return
    
    tcp_socket = socket.socket()
    tcp_socket.connect((host, port))
    print(f"Conectado com {host}:{port}")

    aguarde(1)
    
    tcp_socket.sendall(sonda_nome.encode())
    aguarde(0.5)

    tcp_socket.sendall(file_type.encode())

    data_to_send = f"{file_type}{SEPARATOR}{filename}{SEPARATOR}{filesize}"
    aguarde(1)
    
    tcp_socket.send(data_to_send.encode())

    progress = tqdm.tqdm(range(filesize), f"Enviando: {filename}", unit="B", unit_scale=True, unit_divisor=256)
    with open(filename, "rb") as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                break       
            tcp_socket.sendall(bytes_read)
            progress.update(len(bytes_read))
    
    #os.remove(filename)