import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class formurarioJogo(FlaskForm):
    nome = StringField("nome", [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField("categoria", [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField("console", [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')
    
class formurarioLogin(FlaskForm):
    nickname = StringField("nickname", [validators.DataRequired(), validators.Length(min=1, max=8)])
    usuario = StringField("usuario", [validators.DataRequired(), validators.Length(min=1, max=20)])
    senha = StringField("senha", [validators.DataRequired(), validators.Length(min=1, max=100)])
    salvar = SubmitField('Salvar')

def retornar_capa(id):
    for capa in os.listdir("uploads"):
        if f"imagem-{id}" in capa:
            return capa
        
    return "capa_padrao.jpg"

def delete_capa(id):
    capa = retornar_capa(id)
    if capa != "capa_padrao.jpg":
        os.remove(f"uploads/{capa}")
    