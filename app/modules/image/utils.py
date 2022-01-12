import os
import zipfile

def files_fuction(type_extensions):
    pasta = '/images'

    items = []
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            lista = os.path.join(diretorio, arquivo).split('/')
            extension = str(lista[-1]).split('.')
            if extension[1] == type_extensions: 
                items.append(lista[-1])
    return items


#Verifica se o arquivo existe
def isExists(caminho):
    if os.path.exists(caminho):
            return False
    return True


#Verifica se a extensão é suportada
def isSuported(extension, listExtension):
    exists_extensions = False
    for i in listExtension:
        if extension == i:
            exists_extensions = True
    if exists_extensions == False:
        return False
    return True

#Verifica se o arquivo tem o tamanho maximo
def isMaxTam(caminho, max_bytes):
    if os.path.getsize(caminho) > max_bytes:
            os.remove(caminho)
            return False
    return True

#Cria um arquivo Zip
def create_zip(extension, lista, rate_of_compression = 7):
    if int(rate_of_compression) > 9:
        rate_of_compression = 7

    z = zipfile.ZipFile('final.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=int(rate_of_compression))
  
    for i in lista: 
        z.write(f'./images/{extension}/{i}')