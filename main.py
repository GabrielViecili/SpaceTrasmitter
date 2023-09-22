import rsa, threading, os, socket, datetime, time, hashlib, subprocess, Client_Soc #, Server_soc
from funcoes import limpartela, aguarde, lerString, file_open, file_recente_format, list_files, verificar_chave_enviada, extrair_nome_sonda, verificar_existencia_public_key
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

server_start = subprocess.Popen(["python","Server_soc.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

#verifica se exite a pasta, caso não exista ela cria
pasta_server = "Server"
if not os.path.exists(pasta_server):
    os.makedirs(pasta_server)
pasta_keys = "Keys"
if not os.path.exists(pasta_keys):
    os.makedirs(pasta_keys)

#armazena os nomes, porem ha de fazer uma atualização para que seja armazenado os nomes em um banco de dados de acordo com o usuário
nome_sondas = [] #grava o nome dado a sonda

chave_enviada = bool(nome_sondas)
#limpartela()
print("Seja bem-vindo...")
aguarde(1)

while True:
    #limpartela()
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
        if not verificar_existencia_public_key(pasta_keys) or not nome_sondas:
            print("Digite o nome para cadastrar a nova sonda")
            nome = lerString("nome para a sonda: ").replace(" ","")
            nome_sondas.append(nome)
            print("Aguarde enquanto as chaves são geradas...")
            publicKey = os.path.join(pasta_keys, f"{nome.replace(' ','')}.public.pem")
            privatekey = os.path.join(pasta_keys, f"{nome.replace(' ','')}.private.pem")
            (pubKey, privKey) = rsa.newkeys(2048)
            with open (publicKey, 'wb') as key_file:
                key_file.write(pubKey.save_pkcs1("PEM"))
            with open(privatekey, "wb") as key_file:
                key_file.write(privKey.save_pkcs1("PEM"))
            print("Chaves geradas com sucesso!!")
        else:
            print("Para poder cadastrar nova sonda é necessário enviar a a chave existente")

    elif opcao =="2": #enviar chave a sonda e o server precisa armazena-la como chave certificadora
        if nome_sondas and not verificar_chave_enviada(pasta_keys, nome_sondas[-1]):
            print("Você deseja enviar a chave pública para o servidor? \n  Tecle (1) para confirmar ou (2) para retornar ao Menu")
            option = input()
            try:
                if option == ("1"):
                    sonda_nome = nome_sondas[-1]
                    publickey_path = os.path.join(pasta_keys, f"{sonda_nome}.public.pem")
                    
                    Client_Soc.send_public_key(publickey_path)
                    
                    print("Chave enviada com Sucesso")
                
                elif option ==("2"):
                    print("De volta ao menu")
                else:
                    print("Comando Inválido")
                    input("Pressione enter para continuar")
            except:
                pass
        else:
            print("Não há chaves cadastradas")

    elif opcao =="3": #coletar dados da sonda
        perguntas = ["Local:","Temperatura:", "Radiação Alfa:","Radiação Beta:","Radiação Gama:"] #lista de perguntas
        respostas = [] #lista de respostas
        print("Coleta de dados, favor informar o que solicitado:")
        for pergunta in perguntas: #concatena as perguntas com as respostas
            resposta = input(pergunta + " ")
            respostas.append(resposta)
        print("Valores inseridos com sucesso")
        #date = input("Rcaptcha... Informe a data atual. ") #solicita a data
        dia = datetime.date.today().day
        mes = datetime.date.today().month
        primeira_resposta = respostas [0] #seleciona a primeira resposta para criar o nome do arquivo
        date = (f"{dia}.{mes}")
        nome_do_arquivo = (f"{primeira_resposta}{date}.txt") #concatena o nome do arquivo com a data e salva em txt   
        with open (nome_do_arquivo,"w", encoding="utf-8") as file:
            for pergunta, resposta in zip (perguntas, respostas): #poderia no lugar da função zip fazer um loop com for, que teria o mesmo resultado, porem pelo fato de ja ser nativo do python usarei o zip
                file.write(f"{pergunta}: {resposta}\n")  
        print(f"Dados gravados com sucesso no arquivo '{nome_do_arquivo}'.")
        aguarde(2)
        print("Criptografando os dados...")
        aguarde(2)
        print("Pressione:\n(1) para criar uma chave aleatória\n(2) para criar uma chave manual")
        mensagem = (nome_do_arquivo, "r")
        opcao = input()
        try:
            if opcao == "1": #chave aleatoria       
                key1 = get_random_bytes(16)
                cipher1 = AES.new(key1, AES.MODE_EAX)
                #plaintext1 = mensagem.encode()
                ciphertext, tag = cipher1.encrypt_and_digest(mensagem.encode())
            elif opcao == "2":
                chave = input("Digite a chave desejada: ")
                key2 = chave.encode()
                cipher2 = AES.new(key2, AES.MODE_EAX)
                #plaintext2 = b"" #deve conter os dados a serem criptografados
                ciphertext, tag = cipher2.encrypt_and_digest(mensagem.encode())
            else:#precisa criar uma forma para salvar as chaves criadas
                pass
        except:
            pass
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