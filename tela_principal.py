from tkinter import *
from tkinter import messagebox
from conexao import *
from tkinter import ttk
from novo_gasto import *
#import matplotlib.pyplot as plot
import plotly.graph_objects as go
import datetime
import ctypes

# variável global
global lSaldo

# função para adicionar novos fundos ao saldo
def add_fundos():
    global lSaldo

    # tela de adição de saldo
    tela = Toplevel()
    tela.resizable(0, 0)
    tela["bg"] = "Black"
    tela.geometry('250x100+530+300')

    # função temporária para unir as outras funções
    def temp_func():
        valor = valorF.get()
        valor = valor.replace(',', '.')
        valor = float(valor)

        # confirmação de alteração
        result = messagebox.askquestion("Alerta", "Confirma alteração?", icon = "warning")

        # se sim, adiciono
        if result == 'yes':
            altera_saldo(1, valor)

        # atualizo a label
        saldo = saldo_atual()
        lSaldo["text"] = saldo

    # configurações gerais da tela
    l = Label(tela, text = "Valor:", font = ("Arial", "12"))
    l["fg"] = "White"
    l["bg"] = "Black"
    l.place(x = 10, y = 22)

    valorF = Entry(tela)
    valorF.insert(END, '0,00')
    valorF.place(x = 80, y = 25, width = 140)

    btnOK = Button(tela, text = "OK")
    btnOK["command"] = temp_func
    btnOK["bg"] = "Dark Blue"
    btnOK["fg"] = "White"
    btnOK.place(x = 80, y = 60, width = 80)

# função para atualizar os gastos
def atualiza_gastos():

    # variável global da listbox
    global t_Gastos

    # função para pegar todos os gastos
    aux = select_gastos()

    # limpo a treeview
    t_Gastos.delete(*t_Gastos.get_children())

    # pra cada gasto ele insere as informações na lista
    for i in aux:
        gastos = []
        for u in i:
            gastos.append(u)
        d = gastos[3]
        d_tratado = d.replace('-', '/')
        data = datetime.datetime.strptime(d_tratado, '%Y/%m/%d').strftime("%d/%m/%Y")
        gastos[gastos.index(d)] = data
        t_Gastos.insert("", END, values=gastos)

        # atualizo a label saldo
        saldo = saldo_atual()
        lSaldo["text"] = saldo

# função para deletar os gastos
def del_gastos():

    # variável da lista
    global t_Gastos

    # ele tenta fazer todos os procedimentos
    try:

        # pega o item selecionado na lista
        c = t_Gastos.selection()
        if c == ():
            messagebox.showerror("Atenção", "Não há gastos para deletar!!")
        else:
            # pega os valores do dicionário
            id = []
            for i in c:
                d = t_Gastos.item(i)

                # pega o id
                id.append(d["values"][0])


            # manda uma confirmação
            result = messagebox.askquestion("Alerta", "Confirma alteração?", icon="warning")

            # se a pessoa confirmar, ele exclui e atualiza a lista
            if result == 'yes':
                for i in id:
                    delete_gastos(i)
                atualiza_gastos()

    # se não conseguir ele confere se há algo selecionado na lista
    except Exception as e:
        print(e)
        if str(e) == 'string index out of range':

            # se não houver ele dispara um erro
            messagebox.showerror("Atenção!!", "Selecione ao menos 1 item da lista!!")

# função para gerar o gráfico
def gera_grafico():

    # faço o select dos valores e da data
    v = select("SELECT valor, data FROM gastos ORDER BY data")

    # listas de data e valor
    data = []
    valor = []

    # para cada tupla dentro da lista do select
    for i in v:

        # d recebe a data dentro da tupla
        d = i[1]

        # troco separo os numeros
        d = d.split('-')

        # crio uma nova lista
        a = []

        # adiciono os numeros na nova lista, agora em ordem brasileira dd/mm/yyyy
        a.append(d[2])
        a.append(d[1])
        a.append(d[0])

        # junto a lista com barra
        d = '/'.join(a)

        # recebo o valor como float
        y = float(i[0])

        # por fim, adiciono na lista
        valor.append(y)
        data.append(d)

    # gero o gráfico
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x = data,
        y = valor,
        name = "Valor"
    ))

    fig.update_layout(
        title=go.layout.Title(
            text="Gastos por tempo",
            xref="paper",
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Data",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Valor",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        )
    )
    fig.show()
    # crio o gráfico com a data e o valor
    #ax = plot.plot(data, valor)

    # abro o painel de configurações
    #wm = plot.get_current_fig_manager()

    # configuro a posição na tela que ele aparece
    #wm.window.wm_geometry("700x500+300+150")

    # mostro o gráfico
    #plot.show()


# função para ordenar lista
def order_lista(self):

    # variáveis
    global cmbOrderG, t_Gastos

    # ordenar por descrição
    if cmbOrderG.get() == 'Descricao':

        # select dos gastos ordenados
        aux = select("SELECT * FROM gastos ORDER BY descricao")

        # limpo a treeview
        t_Gastos.delete(*t_Gastos.get_children())

        # pra cada gasto ele insere as informações na lista
        for i in aux:
            gastos = []
            for u in i:
                gastos.append(u)
            d = gastos[3]
            d_tratado = d.replace('-', '/')
            data = datetime.datetime.strptime(d_tratado, '%Y/%m/%d').strftime("%d/%m/%Y")
            gastos[gastos.index(d)] = data
            t_Gastos.insert("", END, values=gastos)

    # ordenar por Maior valor
    elif cmbOrderG.get() == 'Maior Valor':

        # select dos gastos ordenados
        aux = select("SELECT * FROM gastos ORDER BY valor DESC")

        # limpo a treeview
        t_Gastos.delete(*t_Gastos.get_children())

        # pra cada gasto ele insere as informações na lista
        for i in aux:
            gastos = []
            for u in i:
                gastos.append(u)
            d = gastos[3]
            d_tratado = d.replace('-', '/')
            data = datetime.datetime.strptime(d_tratado, '%Y/%m/%d').strftime("%d/%m/%Y")
            gastos[gastos.index(d)] = data
            t_Gastos.insert("", END, values=gastos)

    # ordenar por menor valor
    elif cmbOrderG.get() == 'Menor Valor':

        # select dos gastos ordenados
        aux = select("SELECT * FROM gastos ORDER BY valor")

        # limpo a treeview
        t_Gastos.delete(*t_Gastos.get_children())

        # pra cada gasto ele insere as informações na lista
        for i in aux:
            gastos = []
            for u in i:
                gastos.append(u)
            d = gastos[3]
            d_tratado = d.replace('-', '/')
            data = datetime.datetime.strptime(d_tratado, '%Y/%m/%d').strftime("%d/%m/%Y")
            gastos[gastos.index(d)] = data
            t_Gastos.insert("", END, values=gastos)

    # ordenar pelo gasto mais antigo
    elif cmbOrderG.get() == 'Mais antigo':

        # select dos gastos ordenados
        aux = select("SELECT * FROM gastos ORDER BY strftime('%Y-%m-%d', data)")

        # limpo a treeview
        t_Gastos.delete(*t_Gastos.get_children())

        # pra cada gasto ele insere as informações na lista
        for i in aux:
            gastos = []
            for u in i:
                gastos.append(u)
            d = gastos[3]
            d_tratado = d.replace('-', '/')
            data = datetime.datetime.strptime(d_tratado, '%Y/%m/%d').strftime("%d/%m/%Y")
            gastos[gastos.index(d)] = data
            t_Gastos.insert("", END, values=gastos)

    # ordenar pelo mais recente
    elif cmbOrderG.get() == 'Mais recente':

        # select dos gastos ordenados
        aux = select("SELECT * FROM gastos ORDER BY strftime('%Y-%m-%d', data) DESC")

        # limpo a treeview
        t_Gastos.delete(*t_Gastos.get_children())

        # pra cada gasto ele insere as informações na lista
        for i in aux:
            gastos = []
            for u in i:
                gastos.append(u)
            d = gastos[3]
            d_tratado = d.replace('-', '/')
            data = datetime.datetime.strptime(d_tratado, '%Y/%m/%d').strftime("%d/%m/%Y")
            gastos[gastos.index(d)] = data
            t_Gastos.insert("", END, values=gastos)


# tela principal
def tela(nome):
    global lSaldo, t_Gastos, cmbOrderG

    # criação da tela
    root = Tk()

    # configuração da tela
    root.geometry("800x400+250+200")
    root["bg"] = "Black"
    root.title("Painel de Gastos")
    root.iconbitmap("money.ico")
    root.resizable(0, 0)

    # fonte padrão
    font = ("Arial", "12")

    # nome do usuário
    nome = select_usuario()
    nome = nome[0]

    # saldo atual
    saldo = saldo_atual()

    # label Bom dia
    l = Label(font = ('Arial', '11'))
    l["text"] = "Bom dia " + nome
    l["bg"] = "Black"
    l["fg"] = "White"
    l.place(x = 10, y = 10)

    # label saldo
    l = Label(font = font)
    l["text"] = "Saldo atual: R$ "
    l["bg"] = "Black"
    l["fg"] = "White"
    l.place(x = 20, y = 50)

    # título listas
    l = Label(text = "Lista de Gastos", font = ("Arial", "14", "bold"))
    l["bg"] = "Black"
    l["fg"] = "White"
    l.place(x = 350, y = 45)

    l = Label(text = "Ordenar por: ", font = font)
    l["bg"] = "Black"
    l["fg"] = "White"
    l.place(x = 620, y = 60)

    # valor do saldo
    lSaldo = Label(font = font)
    lSaldo["text"] = saldo
    lSaldo["bg"] = "Black"
    lSaldo["fg"] = "White"
    lSaldo.place(x = 130 , y = 50)

    # groupbox
    lF = LabelFrame(text = "Ações")
    lF["bg"] = "Black"
    lF["fg"] = "White"
    lF.place(x = 10, y = 80, width = 180, height = 300)

    # botão para adicionar fundos a carteira
    btnAddF = Button(lF, font = font)
    btnAddF["text"] = "Adicionar Fundos"
    btnAddF["bg"] = "Dark Blue"
    btnAddF["fg"] = "White"
    btnAddF["command"] = add_fundos
    btnAddF.pack(fill = BOTH, side = TOP, pady = 6, padx = 15)

    # botão para inserir gastos
    btnAddG = Button(lF, font = font)
    btnAddG["text"] = "Inserir Gasto"
    btnAddG["bg"] = "Dark Blue"
    btnAddG["fg"] = "White"
    btnAddG["command"] = inserir_gasto
    btnAddG.pack(fill = BOTH, side = TOP, pady = 5, padx = 15)

    # botão para inserir gastos
    btnDelG = Button(lF, font = font)
    btnDelG["text"] = "Deletar Gasto"
    btnDelG["bg"] = "Dark Blue"
    btnDelG["fg"] = "White"
    btnDelG["command"] = del_gastos
    btnDelG.pack(fill=BOTH, side=TOP, pady=5, padx=15)

    # botão para gerar gráfico
    btnGrafico = Button(lF, font = font)
    btnGrafico["text"] = "Gerar Gráfico"
    btnGrafico["bg"] = "Dark Blue"
    btnGrafico["fg"] = "White"
    btnGrafico["command"] = gera_grafico
    btnGrafico.pack(fill=BOTH, side=TOP, pady=5, padx=15)

    # lista de ordens possíveis
    ordens = ('Mais recente', 'Mais antigo', 'Descricao', 'Maior Valor', 'Menor Valor')

    # combobox para ordenar os gastos
    cmbOrderG = ttk.Combobox(width = 11)
    cmbOrderG["values"] = ordens
    cmbOrderG.place(x = 620, y = 88)
    cmbOrderG.bind("<<ComboboxSelected>>", order_lista)

    # lista de colunas
    colunas = ('ID', 'Descricao', 'Valor R$', 'Data')

    # tabela de gastos
    t_Gastos = ttk.Treeview()

    # tiro a primeira coluna index da lista
    t_Gastos["show"] = "headings"

    # qtd de colunas da base = qtd de colunas da tabela
    t_Gastos["columns"] = colunas

    # criando a fonte do texto
    style = ttk.Style()
    style.configure("Treeview.Heading", font = (None, 10))

    # pra cada coluna eu centralizo o texto, coloco nome e deixo a largura padrão
    for i in colunas:
        t_Gastos.column('#' + str(colunas.index(i) + 1), width = 90, anchor = CENTER)
        t_Gastos.heading('#'+ str(colunas.index(i) + 1), text = i, anchor = CENTER)

    # função para atualizar gastos
    atualiza_gastos()
    t_Gastos.place(x = 250, y = 88)

    btnRefresh = Button(text = "Atualizar", font = font, command = atualiza_gastos)
    btnRefresh["bg"] = "Dark Blue"
    btnRefresh["fg"] = "White"
    btnRefresh.place(x = 400, y = 320)
    root.mainloop()