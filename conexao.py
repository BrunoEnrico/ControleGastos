import sqlite3
import os

# função de select genérico
def select(query):
    con = sqlite3.connect("controle_gastos")
    rs = con.execute(query)
    rs = rs.fetchall()
    con.close()
    return rs

# função de saldo atual
def saldo_atual():
    con = sqlite3.connect("controle_gastos")
    saldo = con.execute("SELECT saldo FROM usuario")
    saldo = saldo.fetchone()
    saldo = saldo[0]
    if saldo.is_integer() == True:
        saldo = int(saldo)
    else:
        saldo = round(saldo, 2)
        saldo = str(saldo)
        saldo = saldo.replace('.', ',')
    con.close()
    return saldo

def altera_saldo(tipo, valor):
    con = sqlite3.connect("controle_gastos")
    saldo = saldo_atual()
    if isinstance(saldo, str) == True:
        saldo = saldo.replace(",", ".")
        saldo = float(saldo)
    if tipo == 1:
        saldo = saldo + valor
    else:
        saldo = saldo - valor
    con.execute("UPDATE usuario SET saldo = " + str(saldo))
    con.commit()
    con.close()

# função para puxar o nome do usuário
def select_usuario():
    con = sqlite3.connect("controle_gastos")
    nome = con.execute("SELECT nome FROM usuario")
    nome = nome.fetchone()
    con.close()
    return nome

# função para puxar os gastos (provavelmente será ajeitada)
def select_gastos():
    con = sqlite3.connect("controle_gastos")
    gastos = con.execute("SELECT * FROM gastos")
    gastos = gastos.fetchall()
    con.close()
    return gastos

# função para inserir um novo usuário utilizando uma lista de dados fornecida
def insert_usuario(dados):

    # dessa lista pego o valor do saldo
    saldo = str(dados[2])

    # trato o numero para padrão americano
    saldo = saldo.replace(",", ".")

    # pego a renda
    renda = str(dados[1])

    # conecto com o banco
    con = sqlite3.connect("controle_gastos")

    # se não houver renda mensal
    if renda == 'None':

        # insiro no banco com valor nulo
        con.execute(
            "INSERT INTO usuario (nome, renda_fixa, saldo) VALUES( '" + dados[0] + "', NULL, " + saldo + ")")

    # caso haja, insiro todos os valores normalmente
    else:
        renda = renda.replace(",", ".")
        con.execute("INSERT INTO usuario (nome, renda_fixa, saldo) VALUES( '" +  dados[0] + "', " + renda +  ", " + saldo + ")")

    # salvo as alterações
    con.commit()

    # fecho a conexão
    con.close()

# inserir novo gasto (provavelmente será alterada)
def insert_gasto(dados):
    try:
        con = sqlite3.connect("controle_gastos")
        con.execute("INSERT INTO gastos (descricao, valor, data) VALUES('" + dados[0] + "', " + dados[1] + ", '" + dados[2] + "')")
        con.commit()
        con.close()
        aux = 1
    except:
        aux = 0
    return aux

# deletar usuário (provavelmente será alterada)
def delete_usuario():
    con = sqlite3.connect("controle_gastos")
    con.execute("DELETE FROM usuario")
    con.commit()
    con.close()

# deletar gasto (provavelmente será alterada)
def delete_gastos(id):
    con = sqlite3.connect("controle_gastos")
    con.execute("DELETE FROM gastos WHERE id = " + str(id))
    con.commit()
    con.close()

# função para verificar se há banco e se há informações nele
def checa_banco():

    # verifico se o banco de dados já existe
    if not os.path.exists("controle_gastos"):

        # crio e conecto com o novo banco de dados
        con = sqlite3.connect("controle_gastos")

        # crio a tabela de usuario
        con.execute("CREATE TABLE usuario (id INTEGER PRIMARY KEY autoincrement NOT NULL, nome TEXT NOT NULL,"
                    " renda_fixa REAL, saldo REAL NOT NULL)")

        # crio a tabela de gastos
        con.execute("CREATE TABLE gastos (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, descricao TEXT NOT NULL,"
                    " valor REAL NOT NULL, data TEXT NOT NULL)")

        # commit
        con.commit()

        # fecho a conexão
        con.close()

    try:
        # verifico se tem valores inseridos
        nome = select_usuario()

    # caso dê algum erro
    except Exception as e:

        # pego o erro
        e = str(e)

        # se for ausência de tabela
        if e.find('such table'):

            # conecto com o banco
            con = sqlite3.connect("controle_gastos")

            # crio a tabela usuário
            try:
                con.execute("CREATE TABLE usuario (id INTEGER PRIMARY KEY autoincrement NOT NULL, nome TEXT NOT NULL,"
                            " renda_fixa REAL, saldo REAL NOT NULL)")
            except:
                pass

            # crio a tabela gastos
            try:
                con.execute("CREATE TABLE gastos (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, descricao TEXT NOT NULL,"
                            " valor REAL NOT NULL, data TEXT NOT NULL)")
            except:
                pass

            # salvo as alterações
            con.commit()

            # fecho a conexão
            con.close()

    # faço um select mesmo que não haja informações
    nome = select_usuario()

    # e retorno os valores
    return nome