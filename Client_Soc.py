import socket
import threading
import tqdm
import os
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
    #print(f"Sonda nome a ser enviado: {sonda_nome}")
    tcp_socket.sendall(sonda_nome.encode())

    file_type = "publickey"

    data_to_send = f"{file_type}{SEPARATOR}{filename}{SEPARATOR}{filesize}"
    aguarde(1)
    #print(f"Conteudo tcp_socket.send a ser enviado: {data_to_send}")
    
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

def send_data(filename, file_type):
    try:
        filesize = os.path.getsize(filename)
    except:
        print("Arquivo não encontrado!")
        return
    
    tcp_socket = socket.socket()
    try:
        tcp_socket.connect((host, port))
        print(f"Conectado com {host}:{port}")

        file_type = "data"

        tcp_socket.send(f"{file_type}{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

        progress = tqdm.tqdm(range(filesize), f"Enviando: {filename}", unit="B", unit_scale=True, unit_divisor=256)
        with open(filename, "rb") as file:
            while True:
                bytes_read = file.read(BUFFER_SIZE)
                if not bytes_read:
                    break       
                tcp_socket.sendall(bytes_read)
                progress.update(len(bytes_read))
        
        os.remove(filename)
    except Exception as e:
        print(f"Erro ao enviar o arquivo: {e}")
    finally:
        tcp_socket.close()


def send_sign(filename,file_type):
    try:
        filesize = os.path.getsize(filename)
    except:
        print("Arquivo não encontrado!")
        return
    
    tcp_socket = socket.socket()
    try:
        tcp_socket.connect((host, port))
        print(f"Conectado com {host}:{port}")

        file_type = "sign"

        tcp_socket.send(f"{file_type}{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

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
    except Exception as e:
        print(f"Erro ao enviar o Arquivo: {e}")
    finally:    
        tcp_socket.close()
    


"""HOST = '127.0.0.1'
PORT = 443

def send_mensage_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("connected \n")

    namefile = str(input("arquivo"))

    client_socket.send(namefile.encode())

    with open(namefile, "wb") as file:
        while True:
            data = client_socket.recv(100000)
            if not data:
                break
            file.write(data)

    print(f"{namefile} recebido \n")
"""