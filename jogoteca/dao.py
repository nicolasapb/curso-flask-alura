from bson.objectid import ObjectId


class JogoDao:
    def __init__(self, db):
        self.__jogos = db.jogos

    @property
    def lista_jogos(self):
        return self.__jogos.find({})

    def cria_jogo(self, novo_jogo):
        jogo = novo_jogo.jogo
        return self.__jogos.insert_one(jogo).inserted_id

    def busca_jogo(self, id_jogo):
        return self.__jogos.find_one({'_id': ObjectId(id_jogo)})

    def atualiza_jogo(self, id_jogo, atualizar_jogo):
        jogo = atualizar_jogo.jogo
        return self.__jogos.update_one({'_id': ObjectId(id_jogo)}, {'$set': jogo}).matched_count

    def remove_jogo(self, id_jogo):
        return self.__jogos.delete_one({'_id': ObjectId(id_jogo)}).deleted_count


class UsuarioDao:
    def __init__(self, db):
        self.__usuarios = db.usuarios

    def cria_usuario(self, novo_usuario):
        usuario = novo_usuario.usuario
        return self.__usuarios.insert_one(usuario).inserted_id

    def busca_usuario(self, id_usuario, senha):
        return self.__usuarios.find_one({'id': id_usuario, 'senha': senha})

    def busca_usuario_por_nome(self, id_usuario):
        return self.__usuarios.find_one({'id': id_usuario})

    def altera_usuario(self, id_usuario, usuario):
        return self.__usuarios.update_one({'_id': ObjectId(id_usuario)}, {'$set': usuario})


class ConsoleDao:
    def __init__(self, db):
        self.__consoles = db.consoles

    @property
    def lista_consoles(self):
        return self.__consoles.find({}).sort("nome", 1)


class CategoriaDao:
    def __init__(self, db):
        self.__categorias = db.categorias

    @property
    def lista_categorias(self):
        return self.__categorias.find({}).sort("nome", 1)
