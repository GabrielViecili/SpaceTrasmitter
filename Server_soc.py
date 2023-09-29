import socket, tqdm, os, threading, rsa

server_host = "127.0.0.1"
server_port = 443

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

def iniciar_server():
    tcp_socket = socket.socket()
    tcp_socket.bind((server_host, server_port))
    tcp_socket.listen()
    print(f"Aguardando conexões para {server_host}:{server_port}")

    key_file = ' '

    while True:
        client_socket, adress = tcp_socket.accept()
        print(f"{adress} foi conectado")
        
        pasta_server = "Server"
        if not os.path.exists(pasta_server):
            os.makedirs(pasta_server)

        def receive_msg():
            nonlocal key_file
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
                    
                    print(f"Arquivo '{filename}' do tipo '{file_type}' recebido com sucesso.")
                
                elif msg_type == "simetrickey":
                    received = client_socket.recv(BUFFER_SIZE).decode()
                    file_type, key_filename, filesize = received.split(SEPARATOR)
                    key_filename = os.path.basename(key_filename)
                    key_filename = ''.join(c for c in key_filename if c.isalnum() or c in '._-')
                    filesize = int(filesize)
                
                    caminho_pasta_server = os.path.join(dir_sonda, key_filename)

                    progress = tqdm.tqdm(range(filesize), f"Recebendo:{key_filename}", unit="B", unit_scale=True, unit_divisor=256)
                    with open(caminho_pasta_server, "wb") as file:
                        while True:
                            bytes_read = client_socket.recv(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            file.write(bytes_read)
                            progress.update(len(bytes_read))
                        
                    print(f"Arquivo '{key_filename}' do tipo '{file_type}' recebido com sucesso.")
                    
                    key_file = key_filename
                    
                elif msg_type == "data":
                    received = client_socket.recv(BUFFER_SIZE).decode()
                    file_type, filename, filesize = received.split(SEPARATOR)
                    filename = os.path.basename(filename)
                    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
                    filesize = int(filesize)

                    caminho_pasta_server = os.path.join(dir_sonda, filename)
                    
                    progress = tqdm.tqdm(range(filesize), f"Recebendo:{filename}", unit="B", unit_scale=True, unit_divisor=256)
                    with open(caminho_pasta_server, "wb") as file:
                        while True:
                            bytes_read = client_socket.recv(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            file.write(bytes_read)
                            progress.update(len(bytes_read))
                    
                    print(f"Arquivo '{filename}' do tipo '{file_type}' recebido com sucesso.")

                elif msg_type == "sign":
                    received = client_socket.recv(BUFFER_SIZE).decode()
                    file_type, filename, filesize = received.split(SEPARATOR)
                    filename = os.path.basename(filename)
                    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
                    filesize = int(filesize)

                    caminho_pasta_server = os.path.join(dir_sonda, filename)

                    progress = tqdm.tqdm(range(filesize), f"Recebendo:{filename}", unit="B", unit_scale=True, unit_divisor=256)
                    with open(caminho_pasta_server, "wb") as file:
                        while True:
                            bytes_read = client_socket.recv(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            file.write(bytes_read)
                            progress.update(len(bytes_read))
                     
                            print(f"Arquivo '{filename}' do tipo '{file_type}' recebido com sucesso.")

                    index = filename.find("assinatura") 
                    if index != -1:
                        data_name = filename[:index]
                    
                    publicKey_path = os.path.join(dir_sonda, f"{sonda_nome}.public.pem")
                    data_path = os.path.join(dir_sonda, f"{data_name}.txt")
                    signature_path = os.path.join(dir_sonda, filename)

                    def file_open(file): 
                        key_file = open(file, 'rb') 
                        key_data= key_file.read() 
                        key_file.close() 
                        return key_data 

                    arquivo = file_open(data_path) 
                    publicKey = rsa.PublicKey.load_pkcs1(file_open(publicKey_path)) 
                    signatureValid = file_open(signature_path) 
                    try:
                        rsa.verify(arquivo, signatureValid, publicKey)
                        print("Arquivo valido com sucesso!")
                    except:
                        print("Essa assinatura não é valida")

                else:
                    print(f"Tipo de mensagem não reconhecido: {file_type}")
            except Exception as e:
                print(f"Erro ao lidar com o cliente: {e}")
            finally:
                pass
                #client_socket.close()

        try:
            receive_thread = threading.Thread(target= receive_msg)
            receive_thread.start()
        except Exception as e:
            print(f"Erro ao iniciar a thread do cliente: {e}")
