from astrapy import DataAPIClient
from datetime import datetime
import time
from tabulate import tabulate

#Função para entrar no database e retorna a datava para ser utilizada pelo código
def entrar_db():
    client = DataAPIClient("AstraCS:kOCujDWZAGtWRICfnUTliKpn:c640f1d1b51ae5b958a2b8ac3e5541c24452916e99aa02a9d579a2d356571ba0")
    db = client.get_database_by_api_endpoint(
    "https://4e652219-3dce-4395-bc8d-38465b7fc0b3-us-east1.apps.astra.datastax.com"
    )

    print(f"Connected to Astra DB: {db.list_collection_names()}")
    return db

#apenas ma função para validar que a data está no formato correto
def formatar_data(data_str):
    while True:
        try:
            data_formatada = datetime.strptime(data_str, "%d/%m/%Y")
            return data_formatada
        except ValueError:
            print("Data inválida. O formato deve ser dd/mm/yyyy.")
            data_str = input("Digite a data novamente (dd/mm/yyyy): ")

#função para cadastrar os livros
def cadastroLivros():
    #entra na database
    db = entrar_db()

    #seleciona a "tabela", livros
    collection = db.livros

    titulo = input("Digite o Título do Livro que deseja inserir no Estoque: ")
    autor = input("Digite o autor do Livro: ")
    genero = input("Digite o genero do Livro: ")
    
    # Verificação para o ano
    while True:
        try:
            ano = int(input("Digite o Ano de Lançamento do Livro: "))
            if ano <= 0:
                raise ValueError("O ano deve ser um número positivo.")
            break
        except ValueError as e:
            print(f"Entrada inválida: {e}. Tente novamente.")

    # Verificação para ISBN
    while True:
        try:
            isbn = int(input("Digite o ISBN do Livro: "))
            if isbn <= 0:
                raise ValueError("O ISBN deve ser um número positivo.")
            break
        except ValueError as e:
            print(f"Entrada inválida: {e}. Tente novamente.")

    # Verificação para quantidade
    while True:
        try:
            quantidade = int(input("Digite a quantidade de Livros no Estoque: "))
            if quantidade < 0:
                raise ValueError("A quantidade não pode ser negativa.")
            break
        except ValueError as e:
            print(f"Entrada inválida: {e}. Tente novamente.")

    #transformando no formato de um documento JSON
    livro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "ano": ano,
        "isbn": isbn,
        "quantidade": quantidade,
    }

    #inserir o livro na "tabela"
    collection.insert_one(livro)
    print("Livro adicionado com sucesso")

#Funçao para cadastrar o cliente
def cadastroCliente():
    db = entrar_db()
    collection = db.clientes

    nome = input("Digite o Nome do Cliente que deseja inserir no Sistema: ")
    email = input("Digite o email do cliente: ")

    nascimento_str = input("Digite a data de nascimento do cliente (dd/mm/aaaa): ")
    nascimento = formatar_data(nascimento_str)

    documento = input("Digite o documento do cliente: ")

    cliente = {
        "nome": nome,
        "e-mail": email,
        "nascimento": nascimento,
        "documento": documento,
    }

    #inserir na tabela "clientes"
    collection.insert_one(cliente)

    print("Cliente cadastrado com sucesso!")

#função para realizar o emprestimo do livro
def emprestimo():
    db = entrar_db()
    collection_emprestimo = db.emprestimo

    #loop para caso de algo errado
    while True:
        try:
            documento = input("Digite o documento do cliente: ")
            tituloLivro = input("Digite o título do Livro: ")

            dataEmprestimo_str = input("Digite a data da retirada do Livro (dd/mm/aaaa): ")

            #Chamando o formatar_data para formatar a data KKKKKKKKKK
            dataEmprestimo = formatar_data(dataEmprestimo_str)

            dataDevolucao_str = input("Digite a data prevista para a devolução do Livro (dd/mm/aaaa): ")
            dataDevolucao = formatar_data(dataDevolucao_str)

            # Verificação para garantir que a data de devolução seja posterior à data de empréstimo
            if dataDevolucao <= dataEmprestimo:
                print("A data de devolução deve ser posterior à data de empréstimo.")
                continue

            emprestimo = {
                "documento": documento,
                "tituloLivro": tituloLivro,
                "dataEmprestimo": dataEmprestimo,
                "dataDevolucao": dataDevolucao,
                "Status": "Pendente",
                "DevolucaoRealizada": ""
            }

            collection_emprestimo.insert_one(emprestimo)

            
            collection_livros = db.livros

            livro = collection_livros.find_one({"titulo": tituloLivro})
            #codigo para alterar a quantidade de livros na tabela livros
            if livro:
                quantidade_atual = int(livro.get("quantidade", 0))

                if quantidade_atual > 0:
                    nova_quantidade = quantidade_atual - 1
                    collection_livros.update_one(
                        {"titulo": tituloLivro}, 
                        {"$set": {"quantidade": nova_quantidade}}
                    )
                    print(f"Empréstimo realizado com sucesso! Quantidade atual de '{tituloLivro}': {nova_quantidade}")
                #VERIFICAÇÕES PARA CASO DE ALGO ERRADO
                else:
                    print(f"Não há exemplares disponíveis para o livro '{tituloLivro}'.")
            else:
                print(f"Livro '{tituloLivro}' não encontrado no banco de dados.")

            break

        except ValueError:
            print("\nEntrada inválida! Certifique-se de inserir os dados corretamente.")
        
        except Exception as e:
            print(f"\nOcorreu um erro: {e}")

        #Caso de algo errado abrirá um input perguntando para ver se o usuario ainda quer fazer a operação
        opcao = input("\nDeseja tentar novamente? (s/n): ").lower()
        if opcao != 's':
            print("Operação de empréstimo cancelada.")
            break

#função para devolução de um livro emprestado
def devolucao():

    db = entrar_db()
    collection = db.emprestimo

    documento = input("Digite o número do documento do cliente: ")
    devolucaoItem_str = input("Digite a data de devolução do livro (dd/mm/aaaa): ")
    devolucaoItem = formatar_data(devolucaoItem_str)

    #código para achar a linha requisitada com base no documento do cliente
    devolucao = collection.find_one({"documento": documento})

    if devolucao is None:
        print("Documento não encontrado.")
        return 

    #codigo para pegar o titulo do livro em questão para realizar a alteração de quantidade
    tituloLivro = devolucao.get("tituloLivro")

    #mudando o Status do emprestimo e colocando a data que a devolução foi feita
    collection.update_one(
        {"documento": documento},
        {"$set": {"Status": "Devolução Realizada", "DevolucaoRealizada": devolucaoItem}}
    )

    #código para realizar a atualizaçao de quantidade
    collection_livros = db.livros
    livro = collection_livros.find_one({"titulo": tituloLivro})

    if livro is None:
        print("Livro não encontrado.")
        return 

    quantidade_atual = livro.get("quantidade", 0)

    #validações
    try:
        quantidade_atual = int(quantidade_atual)
    except ValueError:
        print("Erro ao converter a quantidade para um número inteiro.")
        return 

    #atualizando em um pois só pode emprestar um livro por livro
    nova_quantidade = quantidade_atual + 1
    collection_livros.update_one(
        {"titulo": tituloLivro}, 
        {"$set": {"quantidade": nova_quantidade}}
    )
    print(f"Devolução realizada com sucesso! Quantidade atual de '{tituloLivro}': {nova_quantidade}")

#função para imprimir na tela os livros cadastrados
def listar_livros():
    db = entrar_db()
    collection = db.livros

    #utilizando lista para facilitar na tabulaçao
    livros = []

    for livro in collection.find():
        livros.append(livro)

    if livros:
        #usando a bilbioteca tabulate para imprimir na tela em formato de tabela para melhor compreensão do usuario
        headers = list(livros[0].keys())
        tabela = [[livro.get(h, 'N/A') for h in headers[1:]] for livro in livros]
        print(tabulate(tabela, headers=headers[1:], tablefmt="grid"))
        print("\n\n")
    else:
        print("Nenhum livro encontrado.")

#código para listar os emprestimos em um determinado periodo
def listar_emprestimos():
    db = entrar_db()
    collection = db.emprestimo

    data_inicio_str = input("Digite a data inicial para o filtro (dd/mm/aaaa): ")
    data_inicio = formatar_data(data_inicio_str)

    data_fim_str = input("Digite a data final para o filtro (dd/mm/aaaa): ")
    data_fim = formatar_data(data_fim_str)

    #achar os emprestimo com base nos parametros especificos
    emprestimos = collection.find({"dataEmprestimo":{"$gte": data_inicio, "$lte": data_fim}})

    #Validação para que o filtro não printa nada na tela e sim um aviso    
    if emprestimos.count() == 0:
        print("Nenhum empréstimo encontrado no período especificado.")
        return

    for livro in emprestimos:
        print(livro)

#função para listar os clientes
def listar_clientes():
    db = entrar_db()
    collection = db.clientes
    clientes = []

    for cliente in collection.find():
        clientes.append(cliente)

    #código para formatar como uma tabela
    if clientes:
        headers = list(clientes[0].keys())
        tabela = [[cliente.get(h, 'N/A') for h in headers[1:]] for cliente in clientes]
        print(tabulate(tabela, headers=headers[1:], tablefmt="grid"))
    else:
        print("Nenhum cliente encontrado.")

# Adicionando uma opção de saída
def menu():
    while True:
        print("Menu:")
        print("1. Cadastro de Livros")
        print("2. Cadastro de Clientes")
        print("3. Empréstimo de Livros")
        print("4. Devolução de Livros")
        print("5. Listar Livros")
        print("6. Listar Empréstimos")
        print("7. Listar Clientes")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastroLivros()
        elif opcao == '2':
            cadastroCliente()
        elif opcao == '3':
            emprestimo()
        elif opcao == '4':
            devolucao()
        elif opcao == '5':
            listar_livros()
        elif opcao == '6':
            listar_emprestimos()
        elif opcao == '7':
            listar_clientes()
        elif opcao == '0':
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
