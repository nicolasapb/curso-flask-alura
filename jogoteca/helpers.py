from jogoteca import app
import os


def recupera_image(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nome_arquivo:
            return nome_arquivo


def deleta_arquivo(id):
    arquivo = recupera_image(id)
    if arquivo is not None:
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
