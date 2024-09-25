from astrapy import DataAPIClient
from datetime import datetime
import time

def entrar_db():
    # Initialize the client
    client = DataAPIClient("AstraCS:kOCujDWZAGtWRICfnUTliKpn:c640f1d1b51ae5b958a2b8ac3e5541c24452916e99aa02a9d579a2d356571ba0")
    db = client.get_database_by_api_endpoint(
    "https://4e652219-3dce-4395-bc8d-38465b7fc0b3-us-east1.apps.astra.datastax.com"
    )

    print(f"Connected to Astra DB: {db.list_collection_names()}")

    return db

def formatar_data(data_str):
    while True:
        try:
            # Formato esperado: dd/mm/yyyy
            data_formatada = datetime.strptime(data_str, "%d/%m/%Y")
            return data_formatada
        except ValueError:
            print("Data inválida. O formato deve ser dd/mm/yyyy.")
            data_str = input("Digite a data novamente (dd/mm/yyyy): ")


def cadastroLivros():
    db = entrar_db()

    collection = db.livros

    titulo = input("Digite o Título do Livro que deseja inserir no Estoque: ")
    autor = input("Digite o autor do Livro: ")
    genero = input("Digite o genero do Livro: ")
    ano = int(input("Digite o Ano de Lançamento do Livro: "))
    isbn = int(input("Digite o ISBN do Livro: "))
    quantidade = int(input("Digite a quantidade de Livros no Estoque: "))

    livro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "ano": ano,
        "isbn": isbn,
        "quantidade": quantidade,
    }

    collection.insert_one(livro)
    print("Livro adicionado com sucesso")

def cadastroCliente():

    db = entrar_db()

    collection = db.clientes

    nome = input("Digite o Nome do Cliente que deseja inserir no Sistema: ")
    email = input("Digite o email do cliente: ")

    nascimento_str = input("Digite a data de nascimento do cliente (dd/mm/aaaa): ")
    nascimento = formatar_data(nascimento_str)

    documento = int(input("Digite o documento do cliente: "))
 

    cliente = {
        "nome": nome,
        "e-mail": email,
        "nascimento": nascimento,
        "documento": documento,
    }

    collection.insert_one(cliente)
    print("Cliente cadastrado com sucesso!")


def emprestimo():

    db = entrar_db()

    collection = db.emprestimo

    documento = input(int("Digite o documento do cliente: "))
    tituloLivro = input("Digite o titulo do Livro: ")

    dataEmprestimo_str = input("Digite a data da retirada do Livro (dd/mm/aaaa): ")
    dataEmprestimo = formatar_data(dataEmprestimo_str)

    dataDevolucao_str = input("Digite a data prevista para a devolução do Livro (dd/mm/aaaa): ")
    dataDevolucao = formatar_data(dataDevolucao_str)

 

    cliente = {
        "documento": documento,
        "tituloLivro": tituloLivro,
        "dataEmprestimo": dataEmprestimo,
        "dataDevolucao": dataDevolucao,
        "Status": "Pedente",
        "DevolucaoRealizada": ""
    }

    collection.insert_one(cliente)
    print("Cliente cadastrado com sucesso!")

def devolucao():

    db = entrar_db()

    collection = db.emprestimo

    documento = int(input("Digite o número do documento do cliente: "))

    devolucaoItem_str = input("Digite a data de devolução do livro (dd/mm/aaaa): ")
    devolucaoItem = formatar_data(devolucaoItem_str)

    collection.update_one(
        {"documento": documento},
        {"$set": {"Status": "Devolução Realizada", "DevolucaoRealizada": devolucaoItem}}
    )

def listar_livros():

    db = entrar_db()

    collection = db.livros

    for livro in collection.find():
        print(livro)

def listar_emprestimos():

    db = entrar_db()

    collection = db.emprestimo

    data_inicio_str = input("Digite a data inicial para o filtro (dd/mm/aaaa): ")
    data_inicio = formatar_data(data_inicio_str)

    data_fim_str = input("Digite a data final para o filtro (dd/mm/aaaa): ")
    data_fim = formatar_data(data_fim_str)

    for livro in collection.find({"dataEmprestimo":{"$gte": data_inicio, "$lte": data_fim}
                                  }):
        print(livro)


def listar_clientes():

    db = entrar_db()

    collection = db.clientes

    for cliente in collection.find():
        print(cliente)

def usuarios_com_emprestimos_vencidos():

    db = entrar_db()

    collection = db.emprestimo


    data_atual = datetime.now().strftime("%Y-%m-%d")


    emprestimos_vencidos = collection.find({
        "dataDevolucao": {"$lt": data_atual},  
        "Status": {"$ne": "Devolução Realizada"}  
    })

    print("Usuários com empréstimos vencidos:")
    for emprestimo in emprestimos_vencidos:
        print(f"Cliente: {emprestimo['documento']}, Livro: {emprestimo['tituloLivro']}, Data Devolução Prevista: {emprestimo['dataDevolucao']}, Status: {emprestimo['Status']}")



def menu ():

    print("Bem vindo ao Sistema da Biblioteca\n\n\n")

    while True:

        print("1.Cadastro de Livro")
        print("2.Cadastro Cliente")
        print("3.Realizar um Emprestimo")
        print("4.Realizar uma Devolução")
        print("5. Relatório de Livros")
        print("6. Relatório de Clientes")
        print("7. Relatório de Emprestimos")
        print("8. Clientes com emprestimos vencidos\n\n")

        try:
            escolha = int(input("Escolha uma das opções acima: "))
        except ValueError:
            print("\n\nEntrada inválida! Por favor, digite um número.")
            time.sleep(2)  
            continue

        if escolha == 1:
            cadastroLivros()
            return
        elif escolha == 2:
            cadastroCliente()
            return
        elif escolha == 3:
            emprestimo()
            return
        elif escolha == 4:
            devolucao()
            return
        elif escolha == 5:
            listar_livros()
            return
        elif escolha == 6:
            listar_clientes()
            return
        elif escolha == 7:
            listar_emprestimos()
            return
        
        elif escolha == 8:
            usuarios_com_emprestimos_vencidos()
            return
        
        else:
            print("\n\nResposta inválida! Digite uma resposta válida!\n\n")
            time.sleep(5)

menu()