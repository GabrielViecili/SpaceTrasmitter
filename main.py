import rsa
import threading
import os
import socket
import time
from funcoes import limpartela, aguarde, lerString, file_open
from Server_Client import start_server, start_client

nome_sondas = []
nome_texto = []



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
        break
    elif opcao =="1":
        print("Digite o nome para cadastrar a nova sonda")
        nome = input(str("nome para a sonda: "))
        publickey = nome + "public.pem"
        privatekey = nome + "private.pem"

        (pubKey, privKey) = rsa.newkeys(2048)

        with open (publickey, 'wb') as key_file:
            key_file.write(pubKey.save_pkcs1("PEM"))
        
        with open(privatekey, "wb") as key_file:
            key_file.write(privKey.save_pkcs1("PEM"))

    elif opcao =="2":
        print("Você deseja enviar a chave pública para o servidor? \n  Tecle (1) para confirmar ou (2) para retornar ao Menu")
        option = input()
        if option == ("1"):
            server_socket = start_server() #inicia o socket server
            client_socket = start_client() #inicia o socket cliente
            client_socket.send(publickey.encode()) #envia a msg ao server 
            

            print("Chave enviada com Sucesso")

        elif option ==("2"):
            print("De volta ao menu")
        else:
            print("Comando Inválido")
            input("Pressione enter para continuar")
        break

    elif opcao =="3":
        break

    elif opcao =="4":
        break
    
    elif opcao =="5":
        break
    else:
        print("Comando Inválido")
        input("Pressione enter para continuar")
        aguarde(2)
print("Thanks")