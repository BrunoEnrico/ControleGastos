from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from conexao import *
import datetime

# tupla de gastos
gasto = ()

# listas para as cmb de data
dia = []
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
       "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
ano = []

# for para listar todos os dias no mês
for i in range(31):
    dia.append(i + 1)

# função para mudar o dia caso seja fevereiro
def dias(self):

    # variáveis global
    global cmbMes, cmbDia

    # pego o valor da caixa de mês
    mes = cmbMes.get()

    # se o mês for fevereiro
    if mes == "Fevereiro":

        # deixo a lista em branco
        dia = []

        # listo todos os dias até 28
        for i in range(28):

            # adiciono na lista
            dia.append(i + 1)

        # coloco na cmb
        cmbDia["values"] = dia

    # caso não seja fevereiro, eu listo normalmente de novo
    else:
        dia = []
        for i in range(31):
            dia.append(i + 1)
        cmbDia["values"] = dia

# pegar a data de hoje
aux = datetime.datetime.now()
aux = aux.year

# faço uma lista de anos de até 20 anos
for i in range(21):
    opa = aux - i
    ano.append(opa)

# função do botão OK no gasto
def gasto():

    # variáveis globais
    global txtDesc, txtValor, cmbDia, cmbMes, cmbAno, meses, root

    # lista de informações do gasto
    dados = []

    # pego o valor da descrição
    desc = txtDesc.get()

    # pego o valor do gasto
    valor = txtValor.get()

    # confiro se a descrição está ok
    if desc == '':
        messagebox.showwarning("Atenção", "Descrição em branco!!")
        root.lift()

    # se o valor for 0 eu já disparo um erro
    elif valor == '0,00':
        messagebox.showwarning("Atenção", "Valor do gasto deve ser no mínimo R$ 0,01 !!")
        root.lift()

    # caso não seja
    else:

        # pego o valor da data
        dia = cmbDia.get()
        mes = cmbMes.get()
        ano = cmbAno.get()

        # se alguma caixa estiver vazia eu disparo um erro também
        if dia == '' or mes == '' or ano == '':
            messagebox.showwarning("Atenção", "Datas em branco!!")
            root.lift()

        # caso esteja tudo certo
        else:
            # trato as variáveis
            if int(dia) < 10:
                dia = '0' + str(dia)

            # trato a variável mês
            mes = meses.index(mes) + 1
            if mes < 10:
                mes = '0' + str(mes)
            mes = str(mes)
            data = ano + '-' + mes + '-' + dia
            valor = valor.replace(",", ".")
            valor = float(valor)
            altera_saldo(2, valor)
            valor = str(valor)

            # trato a variável valor
            valor = valor.replace(",", ".")

            # adiciono todas as variáveis na lista de informações
            dados.append(desc)
            dados.append(valor)
            dados.append(data)

            # adiciono no banco
            if insert_gasto(dados) == 1:
                messagebox.showinfo("Atenção", "Gasto inserido com sucesso!!")

            # se o banco retornar algum erro eu aviso
            else:
                messagebox.showwarning("Erro", "Erro ao inserir gasto!!")
                root.lift()

            # fecho a tela
            root.destroy()

# função para inserir gasto
def inserir_gasto():

    global txtDesc, txtData, txtValor, cmbDia, cmbMes, cmbAno, root

    # configurações tela
    root = Tk()
    root.geometry("280x210+500+250")
    root.title("Novo Gasto")
    root.iconbitmap("money.ico")
    root["bg"] = "Black"
    root.resizable(0, 0)
    font = ("Arial", "12")

    # título
    l = Label(root, text = "NOVO GASTO", font = ("Arial", "12", "bold"), bg = "Black", fg = "White")
    l.pack(side = TOP, pady = 5)

    # primeiro container
    frame1 = Frame(root, bg = "Black")
    frame1.pack(side = TOP, fill = X)

    l = Label(frame1, text = "Descrição: ", font = font, bg = "Black", fg = "White")
    l.pack(side = LEFT, padx = 10)

    txtDesc = Entry(frame1)
    txtDesc.pack(side = RIGHT, pady = 10, padx = 10)

    # container 2
    frame2 = Frame(root, bg = "Black")
    frame2.pack(side = TOP, fill = X)

    l = Label(frame2, text = "Valor: ", font = font, bg = "Black", fg = "White")
    l.pack(side = LEFT, pady = 10, padx = 10)

    txtValor = Entry(frame2)
    txtValor.pack(side = RIGHT, pady = 10, padx = 10)
    txtValor.insert(0, '0,00')

    # container 3
    frame3 = Frame(root, bg = "Black")
    frame3.pack(side = TOP, fill = X)

    l = Label(frame3, text = "Data: ", font = font, bg = "Black", fg = "White")
    l.pack(side = LEFT, pady = 10, padx = 10)

    cmbDia = ttk.Combobox(frame3, width = 3, values = dia)
    cmbDia.pack(side = LEFT)

    var = StringVar()
    cmbMes = ttk.Combobox(frame3, width = 11, values = meses, textvariable = var)
    cmbMes.pack(side=LEFT, padx = 4)
    cmbMes.bind("<<ComboboxSelected>>", dias)

    cmbAno = ttk.Combobox(frame3, width = 10, values = ano)
    cmbAno.pack(side = LEFT, padx = 4)

    # botão OK
    btnOK = Button(root, text = "OK", bg = "Dark Blue", fg = "White")
    btnOK["command"] = gasto
    btnOK.pack(fill = X, padx = 80, pady = 10)

    root.mainloop()