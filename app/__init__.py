from genericpath import exists
from flask import Flask, request, jsonify
from .modules.image import FILES_DIRECTORY, EXTENSIONS_LIST, utils
from werkzeug.utils import secure_filename, send_from_directory
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = FILES_DIRECTORY


@app.post('/upload')
def post_file():
    arquivos = request.files
    for key, item in arquivos.items():
        extension = str(item.filename).split('.')[-1]
        caminho = f'./images/{extension}/{item.filename}'

        if not utils.isExists(caminho):
            return {"message": "Arquivo já existe"}, 409

        if not utils.isSuported(extension, EXTENSIONS_LIST):
            return {"message": "Extensão não suportada"}, 415

        item.save(caminho)

        if not utils.isMaxTam(caminho, 1048576):
            return {"message": "Arquivo maior que 1mb"}, 413

    return {"msg": f"Arquivo salvo"}, 201



@app.get('/files')
def list_files():
    items = []

    for diretorio, subpastas, arquivos in os.walk('./images'):
        for arquivo in arquivos:
            lista = os.path.join(diretorio, arquivo).split('/')
            items.append(lista[-1])
    return jsonify(items), 200


@app.get('/files/<extensionsFormat>')
def list_files_by_extension(extensionsFormat):
    if not utils.isSuported(extensionsFormat, EXTENSIONS_LIST): 
        return {"message": "Extensão não permitida"}, 404
    return jsonify(utils.files_fuction(extensionsFormat)), 200

    
@app.get("/download/<name_extension>")
def download(name_extension):
    extension = name_extension.split('.')[-1]

    if not os.path.exists(f'./images/{extension}/{name_extension}'):
        return {"message": "Arquivo não existe"}, 404

    return send_from_directory(directory=f'./images/{extension}', path=f"{name_extension}", as_attachment=True, environ=request.environ), 200


@app.get('/download-zip')
def download_dir_as_zip():
    extension = request.args.get('file_extension')
    rate_of_compression = request.args.get('compression_ratio')
        
    if not utils.isSuported(extension, EXTENSIONS_LIST):
        return {"message": "Extensão não permitida"}, 404
        
    if os.path.exists('./final.zip'):
        os.remove('./final.zip')

    lista = utils.files_fuction(extension)
    utils.create_zip(extension, lista, rate_of_compression)

    
    return send_from_directory(directory='./', path="final.zip", as_attachment=True, environ=request.environ), 200
