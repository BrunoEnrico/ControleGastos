import sqlite3
from tkinter import *
from conexao import *
from tela_principal import *
import novo_cadastro
import os

if __name__ == '__main__':

    nome = checa_banco()
    if nome == None:

        # caso não exista, chamo a função de cadastro de novo usuário
        novo_cadastro.novo_user()

        # pego a lista de dados que a função retornou
        dados = novo_cadastro.dados

        # e insiro os dados digitados no banco com a função de insert
        insert_usuario(dados)

    tela(nome)