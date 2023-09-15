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

def file_recente_format(formato): #função para localizar um arquivo com um formato determinado
    try:
        diretorio = os.getcwd() #obtem o diretorio de trabalho
        archives = os.listdir(diretorio) #lista os arquivos do diretorio
        archives_format = [archive for archive in archives if archive.endswith(formato)] #filtra os arquivos com o formato desejado

        if archives_format: #verifica se existe arquivos com o formato informado
            archive_recent = max(archives_format,key= lambda archive: os.path.getctime(os.path.join(diretorio, archive))) #encontra o arquivo mais recente com o formato fornecido
            return os.path.join(diretorio, archive_recent)
        else:
            return print("nenhum arquivo com o formato desejado foi encontrado")
    except:
        print("Ocorreu um erro...")

def list_files(current_dir):
    file_list = os.listdir(current_dir)
    return file_list