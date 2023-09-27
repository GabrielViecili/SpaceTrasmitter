import socket
import tqdm
import os
import threading
from funcoes import aguarde
from Crypto.Cipher import AES

server_host = "127.0.0.1"
server_port = 443

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"





"""Nomes_sondas = []


def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        print("Recebido:", data.decode().append(Nomes_sondas))

def receive_public_key():
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    progress = tqdm.tqdm(range(filesize), f"Recebendo:{filename}", unit="B", unit_scale=True, unit_divisor=256)
    with open("SERVER-{0}".format(filename), "wb") as file:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            file.write(bytes_read)
            progress.update(len(bytes_read))"""




def iniciar_server():
    tcp_socket = socket.socket()
    tcp_socket.bind((server_host, server_port))
    tcp_socket.listen()
    print(f"Aguardando conexões para {server_host}:{server_port}")

    while True:
        client_socket, adress = tcp_socket.accept()
        print(f"{adress} foi conectado")
        
        pasta_server = "Server"
        if not os.path.exists(pasta_server):
            os.makedirs(pasta_server)

                

        def receive_msg():
            try:
                sonda_nome = client_socket.recv(BUFFER_SIZE).decode()
                
                dir_sonda = os.path.join(pasta_server, sonda_nome)
                if not os.path.exists(dir_sonda):
                    os.makedirs(dir_sonda)

                msg_type = client_socket.recv(BUFFER_SIZE).decode()
                
                if msg_type == "publickey":
                    received = client_socket.recv(BUFFER_SIZE).decode()
                    file_type, filename, filesize = received.split(SEPARATOR)
                    filename = os.path.basename(filename)
                    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
                    filesize = int(filesize)

                    #aguarde(1)
                    #print(f"{received}")
                
                    dir_sonda = os.path.join(pasta_server, sonda_nome)
                    if not os.path.exists(dir_sonda):
                        os.makedirs(dir_sonda)
                
                    caminho_pasta_server = os.path.join(dir_sonda, filename)

                    progress = tqdm.tqdm(range(filesize), f"Recebendo:{filename}", unit="B", unit_scale=True, unit_divisor=256)
                    with open(caminho_pasta_server, "wb") as file:
                        while True:
                            bytes_read = client_socket.recv(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            file.write(bytes_read)
                            progress.update(len(bytes_read))
                        
                    aguarde(5)
                    print(f"Arquivo '{filename}' do tipo '{file_type}' recebido com sucesso.")
                
                elif msg_type == "simetrickey":
                    received = client_socket.recv(BUFFER_SIZE).decode()
                    file_type, filename, filesize = received.split(SEPARATOR)
                    filename = os.path.basename(filename)
                    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
                    filesize = int(filesize)

                    #aguarde(1)
                    #print(f"{received}")
                
                    caminho_pasta_server = os.path.join(dir_sonda, filename)

                    progress = tqdm.tqdm(range(filesize), f"Recebendo:{filename}", unit="B", unit_scale=True, unit_divisor=256)
                    with open(caminho_pasta_server, "wb") as file:
                        while True:
                            bytes_read = client_socket.recv(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            file.write(bytes_read)
                            progress.update(len(bytes_read))
                        
                    aguarde(5)
                    print(f"Arquivo '{filename}' do tipo '{file_type}' recebido com sucesso.")

                elif msg_type == "data":
                    encrypted_data = b""
                    while True:
                        data = client_socket.recv(BUFFER_SIZE)
                        if not data:
                            break
                        encrypted_data += data
                    
                    decipher = AES.new("Chave_simetrica", AES.MODE_EAX, nonce=encrypted_data[:16] )
                    decrypted_data = decipher.decrypt(encrypted_data[16:]) # aqui eu posso usar a tag para poder verificar o arquivo, mas como preciso descriptografar é melhor usar esse comando

                    dados_decrypt = "caminho ou nome a ser definido"
                    with open(dados_decrypt, "w") as file:
                        file.write(decrypted_data)

                    #falta fazer a logica do link

                    received = client_socket.recv(BUFFER_SIZE).decode()
                    file_type, filename, filesize = received.split(SEPARATOR)
                    filename = os.path.basename(filename)
                    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
                    filesize = int(filesize)

                    #aguarde(1)
                    #print(f"{received}")
                
                    caminho_pasta_server = os.path.join(dir_sonda, filename)

                    progress = tqdm.tqdm(range(filesize), f"Recebendo:{filename}", unit="B", unit_scale=True, unit_divisor=256)
                    with open(caminho_pasta_server, "wb") as file:
                        while True:
                            bytes_read = client_socket.recv(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            file.write(bytes_read)
                            progress.update(len(bytes_read))
                        
                    aguarde(5)
                    print(f"Arquivo '{filename}' do tipo '{file_type}' recebido com sucesso.")

                elif msg_type == "sign": #tem que fazer a logica de verificar e depois retornar a mensagem ...
                    
                    received = client_socket.recv(BUFFER_SIZE).decode()
                    file_type, filename, filesize = received.split(SEPARATOR)
                    filename = os.path.basename(filename)
                    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
                    filesize = int(filesize)

                    #aguarde(1)
                    #print(f"{received}")
                
                    caminho_pasta_server = os.path.join(dir_sonda, filename)

                    progress = tqdm.tqdm(range(filesize), f"Recebendo:{filename}", unit="B", unit_scale=True, unit_divisor=256)
                    with open(caminho_pasta_server, "wb") as file:
                        while True:
                            bytes_read = client_socket.recv(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            file.write(bytes_read)
                            progress.update(len(bytes_read))
                        
                    aguarde(5)
                    print(f"Arquivo '{filename}' do tipo '{file_type}' recebido com sucesso.")

                else:
                    print(f"Tipo de mensagem não reconhecido: {file_type}")
            except Exception as e:
                print(f"Erro ao lidar com o cliente: {e}")
            finally:
                client_socket.close()

        try:
            receive_thread = threading.Thread(target= receive_msg)
            receive_thread.start()
        except Exception as e:
            print(f"Erro ao iniciar a thread do cliente: {e}")

    




"""def recv_mensage_client():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 443))
    server_socket.listen()

    client_socket, client_address = server_socket.accept()

    namefile = client_socket.recv(1024).decode()

    with open (namefile, "rb") as file:
        for data in file.readlines():
            client_socket.send(data)

        print("arquivo enviado")"""