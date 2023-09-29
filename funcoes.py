import os, time

def limpartela():
    os.system("cls")

def aguarde(segundos = 1):
    time.sleep(segundos)

def lerString(mensagem):
    while True:
        variavel = input(mensagem)
        if len(variavel)>1:
            return variavel
        else:
            print("Tente novamente")

def file_open(arquivo):
    arquivochave = open(arquivo, 'rb')
    datachave = arquivochave.read()
    arquivochave.close()
    return datachave

def file_recente_format(formato): 
    try:
        diretorio = os.getcwd() 
        archives = os.listdir(diretorio) 
        archives_format = [archive for archive in archives if archive.endswith(formato)] 

        if archives_format: #verifica se existe arquivos com o formato informado
            archive_recent = max(archives_format,key= lambda archive: os.path.getctime(os.path.join(diretorio, archive))) 
            return os.path.join(diretorio, archive_recent)
        else:
            return print("nenhum arquivo com o formato desejado foi encontrado")
    except:
        print("Ocorreu um erro...")

def list_files(current_dir):
    file_list = os.listdir(current_dir)
    return file_list

def extrair_nome_sonda(pasta_keys):
    arquivo_chaves_pub = os.listdir(pasta_keys)

    for arquivo in arquivo_chaves_pub:
        if arquivo.endswitch("public.pem"):
            nome_sonda = os.path.splitext(arquivo)[0]
            nome_sonda.append(nome_sonda)

def verificar_chave_enviada(nome_sonda, pasta_keys):
    public_key_path = os.path.join(pasta_keys, f"{nome_sonda}.public.pem")
    return os.path.exists(public_key_path)

def verificar_existencia_public_key(pasta_keys):
    for filename in os.listdir(pasta_keys):
        if filename.endswith(".public.pem"):
            return True
    return False

def formatar_string(string):
    string = string.strip()
    palavras = string.split()
    palavras_formatadas = [palavra.capitalize() for palavra in palavras]

    string_formatada = "_".join(palavras_formatadas)

    return string_formatada


def adicionar_sonda_bd(sonda):
    with open("Sonda_bd.txt", "r+") as file:
        
        numeros = [int(line.split(" - ")[0])for line in file]
        proximo_numero = max(numeros, default=0) + 1


        file.write(f"{proximo_numero} - {sonda} \n")


def listar_sondas():
    with open("Sonda_bd.txt", "r") as file:
        for line in file:
            print(line.strip())



def selecionar_sonda(numero):
    with open("Sonda_bd.txt", "r") as file:
        for line in file:
            part = line.strip().split(" - ")
            if part[0] == numero:
                return part[1]
                
    return None

def menu_sondas(sonda):
    
    while True:
        print("\n Escolha um opção:")
        print("1 - Adicionar sonda")
        print("2 - Selecionar sonda")
        print("3 - Mostrar sonda selecionada")
        print("0 - Sair")
        
        escolha = input("Opção: ")

        if escolha == "1":
            nome_sonda = input("Digite o nome para a sonda:") 
            formatar_string(nome_sonda)
            adicionar_sonda_bd(nome_sonda)
            print(f"Sonda '{nome_sonda}' adicionada com sucesso. ")
        
        elif escolha == "2":
            listar_sondas()
            numero_sonda = input("Digite o numero da sonda ou pressione (0) para sair ")
            if numero_sonda == "0":
                return menu_sondas
            sonda = selecionar_sonda(numero_sonda)
            if sonda is not None:
                print(f"Sonda selecionada: {sonda}")

                with open("sonda_selecionada.txt","w") as file:
                    file.write(sonda)
            else:
                print("Número Inválido!")
            
        elif escolha == "3":
            print(f"Sondas selecionada: {sonda} ")
            
        elif escolha == "0":
            break
        else:
            print("Opção Inválida. Tente Novamente. ")
        return sonda


        
