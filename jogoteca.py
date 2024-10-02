from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo():
    def __init__(self, nome , categoria, plataforma):
        self.nome = nome
        self.categoria = categoria
        self.plataforma = plataforma
        
    def __str__(self):
        return self.nome
    
class Usuarios():
    def __init__(self, nome , nick, senha):
        self.nome = nome
        self.nick = nick
        self.senha = senha
    
    def __str__(self) -> str:
        return self.nome 
    
usuario1 = Usuarios("Gabriel","Gah","senha1")
usuario2 = Usuarios("Matheus","theu","senha2")
usuario3 = Usuarios("Ana","A","senha3")

users = {
  usuario1.nome : usuario1,   
  usuario2.nome : usuario2,   
  usuario3.nome : usuario3   
}

jogo1 = Jogo("Skyrim", "RPG", "PC")
jogo2 = Jogo("God of War","rack in slach","ps2")
jogo3 = Jogo("Varolant","FPS","Xbox")
lista=[jogo1,jogo2,jogo3]



app = Flask(__name__)

app.secret_key = "Alura"

@app.route('/')
def index():
    if "nome_usuario" not in session or session["nome_usuario"] == None:
        return redirect(url_for("login"))

    return render_template("index.html", titulo= "Jogos", jogos = lista)


@app.route('/novo')
def novo():
    if "nome_usuario" not in session or session["nome_usuario"] == None:
        return redirect(url_for("login", proxima=url_for("novo")))
    
    return render_template("form.html", titulo = "Novo Jogo")

@app.route("/criar", methods = ["POST",])
def criar():
    if "nome_usuario" not in session or session["nome_usuario"] == None:
        return redirect(url_for("login"))
    
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    
    return redirect(url_for("index"))

@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima = proxima)

@app.route("/autenticar", methods = ["POST",])
def autenticar():
    session["nome_usuario"] = request.form["usuario"]
    usuario = request.form["usuario"]
    
    if usuario in users:
        if users[usuario].senha == request.form["senha"]:
            flash(session["nome_usuario"] + " longado com suscesso!")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
        else:
            flash("Erro no login!")
            return redirect(url_for("login"))
        
    # if "senha" != request.form["senha"]:
    #     flash("Erro no login!")
    #     return redirect(url_for("login"))
    # else:
    #     flash(session["nome_usuario"] + " longado com suscesso!")
    #     proxima_pagina = request.form["proxima"]
    #     return redirect(proxima_pagina)

@app.route("/logout")
def logout():
    session["nome_usuario"] = None
    flash("Logout efetuado com suscesso!")
    return redirect(url_for("index"))

app.run(debug=True)