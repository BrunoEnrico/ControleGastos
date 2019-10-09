from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os

# variáveis para controle das informações entre as classes
nome = ''
renda_fixa = ''
dados = []
tela = 0
global root

# função para o botão avançar
def avancar():

    # pego todas as variáveis
    global root, nome_user, nome, l_chama, tela, btnAvancar, btnSair, l

    # se for a primeira tela
    if tela == 0:

        # se a pessoa não digitou nada no campo
        if nome_user.get() == '':

            # ele dispara uma mensagem
            messagebox.showwarning('Alerta!!', "Digite um nome!!")

        # caso ela tenha digitado
        else:

            # pega o texto digitado pela pessoa
            nome = nome_user.get()

            # coloca na lista de informações
            dados.append(nome)

            # marca que essa tela já foi
            tela = tela + 1

            # removo a label Bem vindo
            l.destroy()

            root.geometry("450x130+450+250")
            btnAvancar.place(x=315, y=88, width=80, height=30)
            btnSair.place(x=70, y=88, width=80, height=30)

            # muda o texto da label e do botão
            l_chama["text"] = "Tem alguma renda fixa? Ex: Salário"
            l_chama.place(x = 20, y = 15)

            # crio o radio button
            style = ttk.Style()
            style.configure('Wild.TRadiobutton',
                            background = "Black",
                            foreground = "White",
                            font = ("Arial", "12"))

            a = IntVar()
            rbRenda1 = ttk.Radiobutton(text = "Sim", style = 'Wild.TRadiobutton', value = 1, variable = a)
            rbRenda1.place(x = 50, y = 45)
            rbRenda2 = ttk.Radiobutton(text="Não", style='Wild.TRadiobutton', value = 2, variable = a)
            rbRenda2.place(x=120, y=45)
            a.set(1)

            nome_user.destroy()
            #nome_user.delete(0, 'end')



    # na segunda tela
    elif tela == 1:

        # verifica se foi digitado algum valor
        if nome_user.get() == '':

            # caso não, deduz se que ela não tem renda fixa
            renda_fixa = None
        else:

            # se tiver será adicionado aos dados do usuário
            renda_fixa = nome_user.get()
        dados.append(renda_fixa)

        # marco a passagem de tela
        tela = tela + 1

        # altero os valores para a próxima tela
        l_chama["text"] = "Qual seu saldo atual? R$"
        nome_user.delete(0, 'end')
        nome_user.insert(END, '0,00')
        btnAvancar["text"] = "Concluir"

    elif tela == 2:

        # pego o valor do saldo
        nome = nome_user.get()

        # adiciono aos dados
        dados.append(nome)

        # fecho a tela
        root.destroy()

# função para sair do software
def sair():
    global root
    root.destroy()

# função da interface gráfica da tela de cadastro
def novo_user():
    global root, nome_user, nome, l_chama, tela, btnAvancar, btnSair, l
    root = Tk()
    root.resizable(0, 0)
    root["bg"] = 'Black'
    root.geometry("450x125+450+250")
    root.title('Novo cadastro')
    root.iconbitmap("money.ico")
    font = ("Arial", "12")

    l = Label(text='Bem-vindo!!', font=font, fg = 'White', bg = 'Black')
    l.place(x = 180, y = 5)

    l_chama = Label(text='Como devo te chamar?', font=font, fg = 'White', bg = 'Black')
    l_chama.place(x = 20, y = 45)

    nome_user = Entry()
    nome_user.place(x = 200, y = 47, width = 192)

    btnAvancar = Button(text = 'Avançar', bg = 'Green', fg = 'White', command = avancar)
    btnAvancar.place(x = 315, y = 83, width = 80, height = 30)

    btnSair = Button(text='Sair', bg = 'Red', fg = 'White', command = sair)
    btnSair.place(x = 70, y = 83, width = 80, height = 30)

    root.mainloop()