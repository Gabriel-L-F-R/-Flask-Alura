from flask import render_template, request, redirect, send_from_directory, session, flash, url_for
from helper import delete_capa, retornar_capa, formurarioJogo
from jogoteca import app, db
from models import Jogos
from time import time

segundos = time()

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    # if "nome_usuario" not in session or session["nome_usuario"] == None:
    #     return redirect(url_for("login"))

    return render_template("index.html", titulo= "Jogos", jogos = lista)


@app.route('/novo')
def novo():
    if "nome_usuario" not in session or session["nome_usuario"] == None:
        return redirect(url_for("login", proxima=url_for("index")))
    
    form = formurarioJogo()
    
    return render_template("form.html", titulo = "Novo Jogo", form = form)

@app.route("/criar", methods = ["POST",])
def criar():
    form = formurarioJogo(request.form)
    
    if not form.validate_on_submit():
        flash("Falha na validação!")
        return redirect(url_for("novo"))
    
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    
    check_name = Jogos.query.filter_by(nome=nome).first()
    
    if check_name:
        flash("Jogo já cadastrado!")
        return redirect(url_for("novo"))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    
    arquivo = request.files["arquivo"]
    arquivo.save(f"uploads/imagem-{novo_jogo.id}-{segundos}.jpg")
    
    
    db.session.add(novo_jogo)
    db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/editar/<int:id>")
def editar(id):
    if "nome_usuario" not in session or session["nome_usuario"] == None:
        return redirect(url_for("login", proxima=url_for("index")))
    
    jogo = Jogos.query.filter_by(id=id).first()
    
    form = formurarioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    
    capa = retornar_capa(jogo.id)
    
    return render_template("editar.html", titulo = "Editar Jogo", id=id, capa = capa, form = form)

@app.route("/deletar/<int:id>")
def deletar(id):
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    
    flash("Jogo deletado com suscesso!") 
     
    return redirect(url_for("index"))

@app.route("/atualizar", methods = ["POST",])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form["id"]).first()
    form = formurarioJogo(request.form)
    
    if not form.validate_on_submit():
        flash("Falha na validação!")
        return redirect(url_for("editar", id=jogo.id))
    
    jogo.nome = form.nome.data
    jogo.categoria = form.categoria.data
    jogo.console = form.console.data 
    
    db.session.add(jogo)
    db.session.commit()
    
    arquivo = request.files["arquivo"]
    delete_capa(jogo.id)
    arquivo.save(f"uploads/imagem-{jogo.id}-{segundos}.jpg")
    
    return redirect(url_for("index"))

@app.route("/uploads/<nome_arquivo>")
def imagem(nome_arquivo):
    return send_from_directory("uploads", nome_arquivo)

