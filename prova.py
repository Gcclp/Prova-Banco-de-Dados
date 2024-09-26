from astrapy import DataAPIClient
from datetime import datetime
import time
from tabulate import tabulate

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

    documento = input("Digite o documento do cliente: ")
 

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

    while True:  # Loop contínuo até a finalização ou cancelamento
        try:
            # Coleção de empréstimos
            collection_emprestimo = db.emprestimo

            # Entrada de dados
            documento = input("Digite o documento do cliente: ")
            tituloLivro = input("Digite o título do Livro: ")

            dataEmprestimo_str = input("Digite a data da retirada do Livro (dd/mm/aaaa): ")
            dataEmprestimo = formatar_data(dataEmprestimo_str)

            dataDevolucao_str = input("Digite a data prevista para a devolução do Livro (dd/mm/aaaa): ")
            dataDevolucao = formatar_data(dataDevolucao_str)

            # Dados do empréstimo
            emprestimo = {
                "documento": documento,
                "tituloLivro": tituloLivro,
                "dataEmprestimo": dataEmprestimo,
                "dataDevolucao": dataDevolucao,
                "Status": "Pendente",
                "DevolucaoRealizada": ""
            }

            # Insere o empréstimo na coleção
            collection_emprestimo.insert_one(emprestimo)

            # Coleção de livros
            collection_livros = db.livros

            # Busca o livro pelo título
            livro = collection_livros.find_one({"titulo": tituloLivro})

            if livro:
                # Verifica a quantidade atual
                quantidade_atual = int(livro.get("quantidade", 0))

                if quantidade_atual > 0:
                    # Atualiza a quantidade, subtraindo 1
                    nova_quantidade = quantidade_atual - 1
                    collection_livros.update_one(
                        {"titulo": tituloLivro}, 
                        {"$set": {"quantidade": nova_quantidade}}
                    )
                    print(f"Empréstimo realizado com sucesso! Quantidade atual de '{tituloLivro}': {nova_quantidade}")
                else:
                    print(f"Não há exemplares disponíveis para o livro '{tituloLivro}'.")
            else:
                print(f"Livro '{tituloLivro}' não encontrado no banco de dados.")


            break  # Sai do loop após o sucesso

        except ValueError:
            print("\nEntrada inválida! Certifique-se de inserir os dados corretamente.")
        
        except Exception as e:
            print(f"\nOcorreu um erro: {e}")

        # Oferece uma opção para tentar novamente ou sair
        opcao = input("\nDeseja tentar novamente? (s/n): ").lower()
        if opcao != 's':
            print("Operação de empréstimo cancelada.")
            break

def devolucao():
    db = entrar_db()
    collection = db.emprestimo

    documento = int(input("Digite o número do documento do cliente: "))
    devolucaoItem_str = input("Digite a data de devolução do livro (dd/mm/aaaa): ")
    devolucaoItem = formatar_data(devolucaoItem_str)

    devolucao = collection.find_one({"documento": documento})

    if devolucao is None:
        print("Documento não encontrado.")
        return  # Adiciona um retorno caso o documento não seja encontrado

    tituloLivro = devolucao.get("tituloLivro")

    collection.update_one(
        {"documento": documento},
        {"$set": {"Status": "Devolução Realizada", "DevolucaoRealizada": devolucaoItem}}
    )

    # Coleção de livros
    collection_livros = db.livros

    # Busca o livro pelo título
    livro = collection_livros.find_one({"titulo": tituloLivro})

    if livro is None:
        print("Livro não encontrado.")
        return  # Retorna se o livro não for encontrado

    # Verifica a quantidade atual
    quantidade_atual = livro.get("quantidade", 0)

    # Tenta converter a quantidade para inteiro
    try:
        quantidade_atual = int(quantidade_atual)
    except ValueError:
        print("Erro ao converter a quantidade para um número inteiro.")
        return  # Retorna em caso de erro na conversão

    # Atualiza a quantidade, subtraindo 1
    nova_quantidade = quantidade_atual + 1
    collection_livros.update_one(
        {"titulo": tituloLivro}, 
        {"$set": {"quantidade": nova_quantidade}}
    )
    print(f"Devolução realizada com sucesso! Quantidade atual de '{tituloLivro}': {nova_quantidade}")




def listar_livros():
    db = entrar_db()

    collection = db.livros

    # Lista para armazenar os livros
    livros = []

    # Itera sobre cada livro na coleção e adiciona os dados à lista
    for livro in collection.find():
        livros.append(livro)

    if livros:
        # Pega todas as chaves (headers) dos documentos (campos dos livros)
        headers = list(livros[0].keys())
        
        # Cria uma tabela com os valores correspondentes aos headers para cada livro
        tabela = [[livro.get(h, 'N/A') for h in headers[1:]] for livro in livros]
        
        # Exibe a tabela com os headers dinâmicos
        print(tabulate(tabela, headers=headers[1:], tablefmt="grid"))
        print("\n\n")

    else:
        print("Nenhum livro encontrado.")




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
    # Lista para armazenar os livros
    livros = []

    # Itera sobre cada livro na coleção e adiciona os dados à lista
    for livro in collection.find():
        livros.append(livro)

    if livros:
        # Pega todas as chaves (headers) dos documentos (campos dos livros)
        headers = list(livros[0].keys())
        
        # Cria uma tabela com os valores correspondentes aos headers para cada livro
        tabela = [[livro.get(h, 'N/A') for h in headers[1:]] for livro in livros]
        
        # Exibe a tabela com os headers dinâmicos
        print(tabulate(tabela, headers=headers[1:], tablefmt="grid"))
        print("\n\n")
    else:
        print("Nenhum cliente encontrado.")


def usuarios_com_emprestimos_vencidos():
    db = entrar_db()
    collection = db.emprestimo

    # Obtendo a data atual no formato correto
    data_atual = datetime.now()

    # Filtrando empréstimos vencidos
    emprestimos_vencidos = collection.find({
        "dataDevolucao": {"$lt": data_atual},  # Verifica se a data de devolução é menor que a data atual
        "Status": {"$ne": "Devolução Realizada"}  # Exclui empréstimos que já foram devolvidos
    })

    print("Usuários com empréstimos vencidos:")
    for emprestimo in emprestimos_vencidos:
        # Acessando os dados do empréstimo e formatando a saída
        print(f"Cliente: {emprestimo['documento']}, Livro: {emprestimo['tituloLivro']}, "
              f"Data Devolução Prevista: {emprestimo['dataDevolucao'].strftime('%d/%m/%Y')}, "
              f"Status: {emprestimo['Status']}")

def deletar_info():
    client = entrar_db()

    tabela = input("Digite qual a tabela que queira deletar (livros, clientes ou emprestimo): ").lower()

    tipoDado = input("Digite o filtro para o que deletar (documento ou titulo): ").lower()
    dado = input("Agora digite o valor que deseja deletar: ")

    # Seleciona a coleção/tabela correta
    collection = client.get_collection(tabela)

    # Realiza a operação de deleção
    collection.delete_one({tipoDado: dado})  # `dado` precisa ser o ID do documento

    print(f"Registro com {tipoDado}: {dado} deletado com sucesso!")

def menu():

    print("Bem-vindo ao Sistema da Biblioteca\n\n\n")

    while True:

        print("1. Cadastro de Livro")
        print("2. Cadastro Cliente")
        print("3. Realizar um Empréstimo")
        print("4. Realizar uma Devolução")
        print("5. Relatório de Livros")
        print("6. Relatório de Clientes")
        print("7. Relatório de Empréstimos")
        print("8. Excluir Informações")
        print("9. Clientes com Empréstimos Vencidos")
        print("10. Sair\n\n")

        try:
            escolha = int(input("Escolha uma das opções acima: "))
        except ValueError:
            print("\n\nEntrada inválida! Por favor, digite um número.")
            time.sleep(2)  
            continue  # Continua no loop, exibindo o menu novamente

        if escolha == 1:
            cadastroLivros()
        elif escolha == 2:
            cadastroCliente()
        elif escolha == 3:
            emprestimo()
        elif escolha == 4:
            devolucao()
        elif escolha == 5:
            listar_livros()
        elif escolha == 6:
            listar_clientes()
        elif escolha == 7:
            listar_emprestimos()
        elif escolha == 8:
            deletar_info()
        elif escolha == 9:
            usuarios_com_emprestimos_vencidos()
        elif escolha == 10:
            print("Saindo do sistema.")
            break 
        else:
            print("\n\nResposta inválida! Digite uma resposta válida!\n\n")
            time.sleep(2)

        time.sleep(2) 


menu()