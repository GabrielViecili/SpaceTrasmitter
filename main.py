import rsa, threading, os,  datetime, Client_Soc 
from funcoes import limpartela, aguarde, file_open,  verificar_chave_enviada, verificar_existencia_public_key, formatar_string, menu_sondas
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Server_soc import iniciar_server

server_thread = threading.Thread(target= iniciar_server)
server_thread.start()

pasta_server = "Server"
if not os.path.exists(pasta_server):
    os.makedirs(pasta_server)

pasta_keys = "Keys"
if not os.path.exists(pasta_keys):
    os.makedirs(pasta_keys)
pasta_dados = "Dados"
if not os.path.exists(pasta_dados):
    os.makedirs(pasta_dados)

print("Seja bem-vindo...")
aguarde(1)

try:
    with open ("sonda_selecionada.txt", "r") as file:
        select_sonda = file.read().strip()
except FileNotFoundError:
    select_sonda = " "
if select_sonda:
    print(f"Sonda '{select_sonda}' está selecionada.")
else:
    print(f"Nenhuma sonda selecionada, Por favor selecione uma sonda.")

chave_enviada = bool(select_sonda)
#limpartela()
aguarde(1)

caminho_arquivo = ' '
nome_do_arquivo = ' '
while True:
    
    limpartela()
    print(f"Sonda selecionada: {select_sonda} ")
    print("(0) Sair")
    print("(1) Para Cadastrar a Sonda, ou selecionar uma Sonda")
    print("(2) Gerar Par de Chaves")
    print("(3) Enviar Chave da Sonda")
    print("(4) Coletar Dados da Sonda")
    print("(5) Gerar Assinatura dos dados coletados")
    print("(6) Enviar para a terra os dados")
    opcao = input()
    if opcao == "0":
        print("Até mais!!")
        break
    
    elif opcao == "1":
        select_sonda = menu_sondas(select_sonda)
        with open("sonda_selecionada.txt", "r") as file:
            select_sonda = file.read().strip()

    elif opcao =="2": 
        if not verificar_existencia_public_key(pasta_keys) or not select_sonda:
            print("Aguarde enquanto as chaves são geradas...")
            publicKey = os.path.join(pasta_keys, f"{select_sonda}.public.pem")
            privatekey = os.path.join(pasta_keys, f"{select_sonda}.private.pem")
            (pubKey, privKey) = rsa.newkeys(2048)
            with open (publicKey, 'wb') as key_file:
                key_file.write(pubKey.save_pkcs1("PEM"))
            with open(privatekey, "wb") as key_file:
                key_file.write(privKey.save_pkcs1("PEM"))
            print("Chaves geradas com sucesso!!")
            
        else:
            print("Para poder cadastrar nova sonda é necessário enviar a a chave existente")

    elif opcao =="3":
        if select_sonda and not verificar_chave_enviada(pasta_keys, select_sonda):
            print("Você deseja enviar a chave pública para o servidor? \n  Tecle (1) para confirmar ou (2) para retornar ao Menu")
            option = input()
          
            if option == ("1"):
                nome_sonda_pub = f"{select_sonda}.public.pem"
                publickey_path = os.path.join(pasta_keys, nome_sonda_pub)
                
                Client_Soc.send_public_key(publickey_path, select_sonda)
                aguarde()
            
            elif option ==("2"):
                print("De volta ao menu")
            else:
                print("Comando Inválido")
                input("Pressione enter para continuar")
        else:
            print("Não há chaves cadastradas")

    elif opcao =="4": 
        perguntas = ["Local:","Temperatura:", "Radiação Alfa:","Radiação Beta:","Radiação Gama:"] 
        respostas = [] 
        print("Coleta de dados, favor informar o que solicitado:")
        
        for pergunta in perguntas: 
            resposta = input(pergunta + " ")
            respostas.append(resposta)
        print("Valores inseridos com sucesso")
        
        dia = datetime.date.today().day
        mes = datetime.date.today().month
        primeira_resposta = respostas [0] 
        primeira_resposta_formatada = formatar_string(primeira_resposta)
        date = (f"{dia}.{mes}")
        nome_do_arquivo =  f"{primeira_resposta_formatada}{date}.txt"   
        
        pasta_arquivo = os.path.join(pasta_dados, primeira_resposta_formatada)
        os.makedirs(pasta_arquivo, exist_ok=True)

        dir_arquivo = os.path.join(pasta_arquivo, primeira_resposta_formatada)
        caminho_arquivo = os.path.join(pasta_arquivo, nome_do_arquivo)

        with open (caminho_arquivo,"w", encoding="utf-8") as file:
            for pergunta, resposta in zip (perguntas, respostas): 
                file.write(f"{pergunta}: {resposta}\n")  
        
        print("Pressione:\n(1) para criar uma chave aleatória\n(2) para criar uma chave manual")

        opt = input()
        
        if opt == "1":       
            key = get_random_bytes(16)
            key_random = os.path.join(pasta_arquivo, f"{nome_do_arquivo}.key_random.txt")
            key_random_hex = key #.hex()
            with open (key_random, "wb") as file:
                file.write(key_random_hex)
       
        elif opt == "2":
            chave = input("Digite a chave desejada: ")
            key = chave.encode()
            key_defined = os.path.join(pasta_dados, f"{nome_do_arquivo}.key_defined.txt")
            with open (key_defined, "wb") as file:
                file.write(key)
        
        print(f"Dados gravados com sucesso no arquivo '{caminho_arquivo}'.")
        aguarde(2)
        print("Criptografando os dados...")
        aguarde(2)
        
        cipher = AES.new(key,AES.MODE_EAX)

        with open(caminho_arquivo, 'r') as file:
            mensagem = file.read()

        plaintext = mensagem.encode()
 
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        ciphertext_hex = ciphertext #.hex()
        tag_hex = tag #.hex()

        with open(caminho_arquivo, 'wb') as file:
            file.write(ciphertext_hex)

        tag_autentic = os.path.join(pasta_arquivo, f"{os.path.basename(nome_do_arquivo)}_tag.txt")

        with open(tag_autentic, "wb") as file:
            file.write(tag_hex)

        #print("Key:", key)
        #print("Texto cifrado:", ciphertext_hex) 
        #print("Tag de autenticação:", tag_hex)
        #print("Dados criptografados com sucesso")

    elif opcao =="5": 
        keyprivate_name = f"{select_sonda}.private.pem"
        privatekey_path = os.path.join(pasta_keys, f"{select_sonda}.private.pem")
        keyprivate = rsa.PrivateKey.load_pkcs1(file_open(privatekey_path))
        
        arquivo_path = os.path.join(caminho_arquivo)
        arquivo_hash = file_open(arquivo_path)
        hash_value = rsa.compute_hash(arquivo_hash, 'SHA-512')
        
        #print("HASH:",hash_value.hex() )
        #print(caminho_arquivo)
        #print(arquivo_hash)
        #print(keyprivate)

        arquivo_signature = f"{primeira_resposta_formatada}{date}assinatura"

        caminho_signature = os.path.join(os.path.dirname(arquivo_path), arquivo_signature)

        msg_ass = f"{select_sonda}{hash_value}"
        assinatura = rsa.sign(arquivo_hash, keyprivate, "SHA-512") # aqui esta o problema

        with open(caminho_signature, "wb") as s:
            s.write(assinatura)
        
        print("Assinatura gerada com sucesso!")
        aguarde(1)

        #print("Assinatura:", binascii.hexlify(assinatura))
        #print("Tamanho da assinatura:", len(assinatura))
        #print("Tamanho do Hash:", len(hash_value))

    elif opcao =="6": #enviar para a terra os dados
        sign_path = os.path.join(pasta_arquivo, f"{arquivo_signature}")
        data_path = os.path.join(pasta_arquivo, f"{nome_do_arquivo}")
        key_path = key_random

        Client_Soc.send_arquivs(key_path, select_sonda, "simetrickey")
        aguarde()
        Client_Soc.send_arquivs(data_path, select_sonda, "data")
        aguarde()
        Client_Soc.send_arquivs(sign_path, select_sonda, "sign")
        aguarde(2)
       
    else:
        print("Comando Inválido")
        input("Pressione enter para continuar")
        aguarde(2)
print("Thanks")