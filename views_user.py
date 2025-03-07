from flask import render_template, request, redirect, session, flash, url_for
from helper import formurarioLogin
from jogoteca import app
from models import Usuarios
from flask_bcrypt import check_password_hash



@app.route("/login")
def login():
    form = formurarioLogin()
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima = proxima, form = form)

@app.route("/autenticar", methods = ["POST",])
def autenticar():
    form = formurarioLogin(request.form)
    if not form.validate_on_submit():
        flash("Falha na validação!")
        return redirect(url_for("login"))
    
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    
    if usuario and senha:
        session["nome_usuario"] = form.nickname.data
        flash(session["nome_usuario"] + " longado com suscesso!")
        proxima_pagina = request.form["proxima"]
        return redirect(proxima_pagina)

    flash("Usuario não encontrado!")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session["nome_usuario"] = None
    flash("Logout efetuado com suscesso!")
    return redirect(url_for("index"))