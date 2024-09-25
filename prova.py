from astrapy import DataAPIClient
import datetime


def db():
    # Initialize the client
    client = DataAPIClient("AstraCS:kOCujDWZAGtWRICfnUTliKpn:c640f1d1b51ae5b958a2b8ac3e5541c24452916e99aa02a9d579a2d356571ba0")
    db = client.get_database_by_api_endpoint(
    "https://4e652219-3dce-4395-bc8d-38465b7fc0b3-us-east1.apps.astra.datastax.com"
    )

    print(f"Connected to Astra DB: {db.list_collection_names()}")

    return db

def cadastroLivros():
    db = db()

    collection = db.livros

    titulo = input("Digite o Título do Livro que deseja inserir no Estoque: ")
    autor = input("Digite o autor do Livro: ")
    genero = input("Digite o genero do Livro: ")
    ano = input(int("Digite o Ano de Lançamento do Livro: "))
    isbn = input(int("Digite o ISBN do Livro: "))
    quantidade = input(int("Digite a quantidade de Livros no Estoque: "))

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
    db = db()

    collection = db.clientes

    nome = input("Digite o Nome do Cliente que deseja inserir no Sistema: ")
    email = input("Digite o email do cliente: ")
    nascimento = input("Digite a data de nascimento do cliente: ")
    documento = input(int("Digite o documento do cliente: "))
 

    cliente = {
        "nome": nome,
        "e-mail": email,
        "nascimento": nascimento,
        "documento": documento,
    }

    collection.insert_one(cliente)
    print("Cliente cadastrado com sucesso!")


def emprestimo():

    db = db()

    collection = db.emprestimo

    documento = input(int("Digite o documento do cliente: "))
    tituloLivro = input("Digite o Titulo do Livro que será emprestado: ")
    dataEmprestimo = input("Digite a data da retirada do Livro: ")
    dataDevolucao = input("Digite a data prevista para a devolução do Livro: ")

 

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

    db = db()

    collection = db.emprestimo

    documento = input(int("Digite o número do documento do cliente: "))
    devolucaoItem = input("Digite a data de devolução do livro: ")

    collection.update_one(
        {"documento": documento},
        {"$set": {"Status": "Devolução Realizada", "DevolucaoRealizada": devolucaoItem}}
    )

def listar_livros():

    db = db()

    collection = db.livros

    for livro in collection.find():
        print(livro)

def listar_emprestimos():

    db = db()

    collection = db.emprestimo

    documento = input("Digite o documento do cliente: ")


    for livro in collection.find({"documento": documento}):
        print(livro)


# collection = db.clientes

# db = db()

# collection = db.emprestimo
# # print("Tabela 'musicas' criada com sucesso!")

# # Inserir uma nova música
# replaced_musica = collection.find_one_and_replace(
#     {"_id": "1b40be54-fa44-462b-80be-54fa44162bae"},
#     {"id": "1", "documento": "Nova Música", "tituloLivro": "dataEmprestimo", "dataDevolucao": "Novo Gênero", "Status": "Pendente", "DevolucaoRealizada": ""}
# )
# print("Música substituída:", replaced_musica)

db = db()

collection = db.emprestimo

documento = input("Digite o documento do cliente: ")


for livro in collection.find({"documento": documento}):
    print(livro)