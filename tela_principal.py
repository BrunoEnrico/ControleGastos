from tkinter import *
from tkinter import messagebox
from conexao import *
from tkinter import ttk
from novo_gasto import *
import ctypes

# variável global
global lSaldo

# função para adicionar novos fundos ao saldo
def add_fundos():
    global lSaldo

    # tela de adição de saldo
    tela = Toplevel()
    tela.resizable(0, 0)
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
            adiciona_fundos(1, valor)

        # atualizo a label
        saldo = saldo_atual()
        lSaldo["text"] = saldo

    # configurações gerais da tela
    l = Label(tela, text = "Valor:", font = ("Arial", "12"))
    l.place(x = 10, y = 22)

    valorF = Entry(tela)
    valorF.insert(END, '0,00')
    valorF.place(x = 80, y = 25, width = 140)

    btnOK = Button(tela, text = "OK")
    btnOK["command"] = temp_func
    btnOK.place(x = 80, y = 60, width = 80)

# função para atualizar os gastos
def atualiza_gastos():

    # variável global da listbox
    global t_Gastos

    # função para pegar todos os gastos
    gastos = select_gastos()

    # limpo a treeview
    t_Gastos.delete(*t_Gastos.get_children())

    # pra cada gasto ele insere as informações na lista
    for i in gastos:
        t_Gastos.insert("", END, values = i)

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
        c = t_Gastos.focus()

        # pega os valores do dicionário
        d = t_Gastos.item(c)

        # pega o id
        id = d["values"][0]

        # manda uma confirmação
        result = messagebox.askquestion("Alerta", "Confirma alteração?", icon="warning")

        # se a pessoa confirmar, ele exclui e atualiza a lista
        if result == 'yes':
            delete_gastos(id)
            atualiza_gastos()

    # se não conseguir ele confere se há algo selecionado na lista
    except Exception as e:
        if str(e) == 'string index out of range':

            # se não houver ele dispara um erro
            messagebox.showerror("Atenção!!", "Selecione ao menos 1 item da lista!!")

# função para ordenar lista
def order_lista(self):
    global cmbOrderG, t_Gastos
    if cmbOrderG.get() == 'Descricao':

        gastos = select("SELECT * FROM gastos ORDER BY descricao")

        # limpo a treeview
        t_Gastos.delete(*t_Gastos.get_children())

        # pra cada gasto ele insere as informações na lista
        for i in gastos:
            t_Gastos.insert("", END, values=i)


# tela principal
def tela(nome):
    global lSaldo, t_Gastos, cmbOrderG

    # criação da tela
    root = Tk()

    # configuração da tela
    root.geometry("800x400+250+200")
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
    l.place(x = 10, y = 10)

    # label saldo
    l = Label(font = font)
    l["text"] = "Saldo atual: R$ "
    l.place(x = 20, y = 50)

    # título listas
    l = Label(text = "Lista de Gastos", font = ("Arial", "14", "bold"))
    l.place(x = 350, y = 45)

    l = Label(text = "Ordenar por: ", font = font)
    l.place(x = 620, y = 60)

    # valor do saldo
    lSaldo = Label(font = font)
    lSaldo["text"] = saldo
    lSaldo.place(x = 130 , y = 50)

    # groupbox
    lF = LabelFrame(text = "Ações")
    lF.place(x = 10, y = 80, width = 180, height = 300)

    # botão para adicionar fundos a carteira
    btnAddF = Button(lF, font = font)
    btnAddF["text"] = "Adicionar Fundos"
    btnAddF["command"] = add_fundos
    btnAddF.pack(fill = BOTH, side = TOP, pady = 6, padx = 15)

    # botão para inserir gastos
    btnAddG = Button(lF, font = font)
    btnAddG["text"] = "Inserir Gasto"
    btnAddG["command"] = inserir_gasto
    btnAddG.pack(fill = BOTH, side = TOP, pady = 5, padx = 15)

    # botão para inserir gastos
    btnDelG = Button(lF, font=font)
    btnDelG["text"] = "Deletar Gasto"
    btnDelG["command"] = del_gastos
    btnDelG.pack(fill=BOTH, side=TOP, pady=5, padx=15)


    # lista de ordens possíveis
    ordens = ('Mais recente', 'Data', 'Descricao', 'Valor')

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
    btnRefresh.place(x = 400, y = 320)
    root.mainloop()