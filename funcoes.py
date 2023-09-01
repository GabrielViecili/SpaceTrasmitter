import os
import time


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