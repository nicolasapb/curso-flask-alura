from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogo, Usuario
from dao import JogoDao, UsuarioDao, ConsoleDao, CategoriaDao
from jogoteca import app, db
from helpers import recupera_image, deleta_arquivo
import time

jogoDao = JogoDao(db)
usuarioDao = UsuarioDao(db)
consoleDao = ConsoleDao(db)
categoriaDao = CategoriaDao(db)


@app.route('/')
def index():
    lista = []
    for _jogo in jogoDao.lista_jogos:
        lista.append(Jogo(_jogo['nome'], _jogo['categoria'], _jogo['console'], _jogo['_id']))
    return render_template('lista.html', titulo=f'jogos - total: {len(lista)}', jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    consoles = []
    for console in consoleDao.lista_consoles:
        consoles.append({'nome': console['nome']})
    categorias = []
    for categoria in categoriaDao.lista_categorias:
        categorias.append({'nome': categoria['nome']})
    return render_template('novo.html', titulo='Novo Jogo', capa_jogo=f'capa_padrao2.jpg',
                           consoles=consoles, categorias=categorias)


@app.route('/criar', methods=['POST', ])
def criar():
    if request.form['nome']:
        arquivo = request.files['arquivo']
        novo_jogo = Jogo(request.form['nome'], request.form['categoria'], request.form['console'])
        id_jogo = jogoDao.cria_jogo(novo_jogo)
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        arquivo.save(f'{upload_path}/capa_{id_jogo}_{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogoDao.busca_jogo(id)
    jogo_id = jogo['_id']
    nome_imagem = recupera_image(jogo_id)
    if nome_imagem is None:
        nome_imagem = 'capa_padrao2.jpg'
    consoles = []
    for console in consoleDao.lista_consoles:
        consoles.append({'nome': console['nome']})
    categorias = []
    for categoria in categoriaDao.lista_categorias:
        categorias.append({'nome': categoria['nome']})
    return render_template('editar.html', titulo='Alterar Jogo', jogo=jogo, capa_jogo=nome_imagem,
                           consoles=consoles, categorias=categorias)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    atualziar_jogo = Jogo(request.form['nome'], request.form['categoria'], request.form['console'])
    atualizados = jogoDao.atualiza_jogo(request.form['id'], atualziar_jogo)
    if 'arquivo' in request.files:
        upload_path = app.config['UPLOAD_PATH']
        jogo_id = request.form['id']
        arquivo = request.files['arquivo']
        timestamp = time.time()
        deleta_arquivo(jogo_id)
        arquivo.save(f'{upload_path}/capa_{jogo_id}_{timestamp}.jpg')

    if atualizados:
        flash('Jogo atualizado com sucesso!')
    return redirect(url_for('index'))


@app.route('/deletar/<id>')
def deletar(id):
    deletado = jogoDao.remove_jogo(id)
    if deletado:
        deleta_arquivo(id)
        flash('Jogo removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    if 'usuario_logado' in session and session['usuario_logado'] is not None:
        return redirect(url_for('index'))
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, titulo='Faça seu login')


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuarioDao.busca_usuario(request.form['usuario'], request.form['senha'])
    if usuario is not None:
        session['usuario_logado'] = usuario['id']
        flash('Bem vindo, ' + usuario['nome'] + '!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha inválidos!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Bye!')
    return redirect(url_for('login'))


@app.route('/signup')
def signup():
    return render_template('signup.html', titulo='Bem vindo!')


@app.route('/criar_usuario', methods=['POST', ])
def criar_usuario():
    novo_usuario = Usuario(request.form['usuario'], request.form['nome'], request.form['sobrenome'],
                           request.form['senha'], request.form['email'])
    criado = usuarioDao.cria_usuario(novo_usuario)
    if criado:
        flash('Usuário cadastrado com sucesso!')
    return redirect(url_for('login'))


@app.route('/modificar_usuario')
def modificar_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar')))
    usuario = usuarioDao.busca_usuario_por_nome(session['usuario_logado'])
    return render_template('alterar_usuario.html', usuario=usuario)


@app.route('/salvar_usuario', methods=['POST', ])
def salvar_usuario():
    alterar_usuario = {'id': request.form['usuario'], 'nome': request.form['nome'],
                       'sobrenome': request.form['sobrenome'], 'email': request.form['email']}
    alterado = usuarioDao.altera_usuario(request.form['id'], alterar_usuario)
    if alterado:
        flash('Modificações salvas')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', filename=nome_arquivo)
