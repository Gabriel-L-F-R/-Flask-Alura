from urllib.parse import quote_plus

senha = "admin"
senha_codificada = quote_plus(senha)

SECRET_KEY = "Alura"

SQLALCHEMY_DATABASE_URI = \
    "{SGBD}://{usuario}:{senha}@{servidor}/{database}".format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = senha_codificada,
        servidor = 'localhost',
        database = 'jogoteca'
    )