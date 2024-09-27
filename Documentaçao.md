- Código desenvolvido por Gabriel Palhano e Eduardo Nogaroto -

  O sistema desenvolvido permite o cadastro e empréstimo de livros para uma biblioteca, utilizando
  Python e um banco de dados não relacional Cassandra. O sistema permite a
  inserção, consulta e atualização de informações sobre livros, usuários e empréstimos, além de realizar operações CRUD

  Ele gerencia uma biblioteca que realiza o cadastro de livros e usuários, além de controlar os empréstimos e devoluções dos livros. O sistema armazena
essas informações em um banco de dados não relacional Cassandra sendo um banco colunar.

- Manual rápido de utilização

Quando executado o código, através das opções:

Digitando 1 para Cadastro de Livros:
Permite cadastrar um livro com as informações como título, autor, gênero, ano de publicação, ISBN e quantidade de exemplares disponíveis


Digitando 2 para Cadastro de Clientes:
Permite o cadastro de usuários com nome, e-mail, data de nascimento e número de documento.


Digitando 3	para Empréstimo de Livros:
Ao solicitar um empréstimo, o sistema verificará a disponibilidade do livro e registrará a operação, associando-o ao usuário e atualizando a quantidade de exemplares disponíveis. 
As datas de empréstimo e previsão de devolução também serão registradas.


Digitando 4	para Devoluções: 
Ao devolver um livro, o sistema atualizará a quantidade de exemplares disponíveis e registrará a data da devolução.


Digitando 5 para Listar Livros:
lista livros disponíveis,

Digitando 6 para Listar Empréstimos:
consultar os empréstimos de um usuário específico e verificar quais usuários possuem empréstimos

Digitando 7 para Listar Clientes:
Listar Clientes

Digitando 0 - Para sair
