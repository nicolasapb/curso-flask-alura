class Jogo:

    def __init__(self, nome, categoria, console, key=None):
        self.__id = key
        self.__nome = nome
        self.__categoria = categoria
        self.__console = console

    @property
    def nome(self):
        return self.__nome

    @property
    def categoria(self):
        return self.__categoria

    @property
    def console(self):
        return self.__console

    @property
    def id(self):
        return self.__id

    @property
    def jogo(self):
        return {'nome': self.__nome, 'categoria': self.__categoria, 'console': self.__console}


class Usuario:

    def __init__(self, id, nome, sobrenome, senha, email=None):
        self.__id = id
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__senha = senha
        self.__email = email

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def senha(self):
        return self.__senha

    @property
    def email(self):
        return self.__email

    @property
    def sobrenome(self):
        return self.__sobrenome

    @property
    def usuario(self):
        return {'id': self.__id, 'nome': self.__nome, 'sobrenome': self.__sobrenome,
                'senha': self.__senha, 'email': self.__senha}
