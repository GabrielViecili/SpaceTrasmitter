import rsa, threading, os, socket, datetime, time, hashlib
from funcoes import limpartela, aguarde, lerString, file_open, file_recente_format, list_files
from Client import start_client, play_server
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

nome_sondas = [] #grava o nome dado a sonda
nome_texto = [] # grava bosta nenhuma

limpartela()
print("Seja bem-vindo...")
aguarde(1)

while True:
    limpartela()
    print("(0) Sair")
    print("(1) Cadastrar Sonda e Gerar Par de Chaves")
    print("(2) Enviar Chave da Sonda")
    print("(3) Coletar Dados da Sonda")
    print("(4) Gerar Assinatura dos dados coletados")
    print("(5) Enviar para a terra os dados")
    opcao = input()
    if opcao == "0":
        print("Até mais!!")
        break

    elif opcao =="1": # cadastrar sonda e gerar par de chaves
        print("Digite o nome para cadastrar a nova sonda")
        nome = lerString("nome para a sonda: ")
        nome = nome.replace(" ","")
        print("Aguarde enquanto as chaves são geradas...")
        publicKey = nome.replace(" ","") + "public.pem"
        privatekey = nome.replace(" ","") + "private.pem"
        (pubKey, privKey) = rsa.newkeys(2048)
        with open (publicKey, 'wb') as key_file:
            key_file.write(pubKey.save_pkcs1("PEM"))
        with open(privatekey, "wb") as key_file:
            key_file.write(privKey.save_pkcs1("PEM"))
        
        print("Chaves geradas com sucesso!!")

    elif opcao =="2": #enviar chave a sonda e o server precisa armazena-la como chave certificadora
        print("Você deseja enviar a chave pública para o servidor? \n  Tecle (1) para confirmar ou (2) para retornar ao Menu")
        option = input()
        try:
            if option == ("1"):
                server_socket = play_server() #inicia o socket server
                client_socket = start_client() #inicia o socket cliente
                client_socket.send(publicKey.encode()) #envia a msg ao server 
                    

                
                print("Chave enviada com Sucesso")
            
            elif option ==("2"):
                print("De volta ao menu")
            else:
                print("Comando Inválido")
                input("Pressione enter para continuar")
        except:
            print("Valor inserido incorretamente")

    elif opcao =="3": #coletar dados da sonda
        perguntas = ["Local:","Temperatura:", "Radiação Alfa:","Radiação Beta:","Radiação Gama:"] #lista de perguntas
        respostas = [] #lista de respostas
        primeira_resposta = respostas [0] #seleciona a primeira resposta para criar o nome do arquivo
        print("Coleta de dados, favor informar o que solicitado:")
        for pergunta in perguntas: #concatena as perguntas com as respostas
            resposta = input(pergunta + " ")
            respostas.append(resposta)
            print("Valores inseridos com sucesso")
        #date = input("Rcaptcha... Informe a data atual. ") #solicita a data
        dia = datetime.date.today().day
        mes = datetime.date.today().month
        date = (f"{dia}.{mes}")
        nome_do_arquivo = (f"{primeira_resposta}{date}.txt") #concatena o nome do arquivo com a data e salva em txt   
        with open (primeira_resposta+date,"w") as file:
            for pergunta, resposta in zip (perguntas, respostas): #poderia no lugar da função zip fazer um loop com for, que teria o mesmo resultado, porem pelo fato de ja ser nativo do python usarei o zip
                file.write(f"{pergunta}: {resposta}\n")  
        mensagem = (nome_do_arquivo, "r")
        plaintext = mensagem.encode()
        print(f"Dados gravados com sucesso no arquivo '{nome_do_arquivo}'.")
        print("Criptografando os dados...")
        print("Pressione:\n(1) para criar uma chave aleatória\n(2) para criar uma chave manual")
        opcao = input()
        if opcao == "1": #chave aleatoria
            key1 = get_random_bytes(16)
            cipher1 = AES.new(key1, AES.MODE_EAX)
            ciphertext, tag = cipher1.encrypt_and_digest(plaintext)
        elif opcao == "2":
            chave = input("Digite a chave desejada: ")
            key2 = b"chave"
            cipher2 = AES.new(key2, AES.MODE_EAX)
            ciphertext, tag = cipher2.encrypt_and_digest(plaintext)
            #formato_desejado = (chave)
            #arquivo_recente = file_recente_format(formato_desejado)
# criptografar os dados do arquivo com uma chave AES a ser definida pelo aluno

    elif opcao =="4": #gerar assinatura dos dados coletados
        #faz o hash
        sha256 = hashlib.sha256()
        data = open(" ","rb")
        sha256.update(data.read())

        print("SHA1: {0}". format(sha256.hexdigest()))
        
        arquivo_hash = file_open() #()inserir o nome do arquivo...
        hash_value = rsa.compute_hash(arquivo_hash, 'SHA-256')
        print("HASH:",hash_value.hex() )

        assinatura = rsa.sign(arquivo_hash, privatekey, "SHA-512")
        s = open("signature_file","wb")
        s.write( assinatura)
        s.close()

    elif opcao =="5": #enviar para a terra os dados
        break
    else:
        print("Comando Inválido")
        input("Pressione enter para continuar")
        aguarde(2)
print("Thanks")