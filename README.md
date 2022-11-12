# Exercício Flask

Construir uma APIRestful (utilizando flask) para controlar uma agenda de contatos:

1 - Criar a base de dados agenda.db em SQLite.

2 - Criar a tabela contatos (id, nome, empresa, telefone, email)

3 - Implementar CRUD completo

Criar contato (Método POST -> INSERT no database)
Recuperar contato (Método GET -> SELECT no database)
Atualizar contato (Método PUT -> UPDATE no database)
Deletar contato (Método DELETE -> DELETE no database)


4 - Implementar ao menos as seguintes consultas:
por nome
por empresa
por email
OBS: As consultas devem ser feitas de forma que seja possível consultar por coincidência exata ou parcial


5 - Criar segundo endpoint filtrando os contatos por empresa e use o protocolo http (404) em caso de falha.
6 - Criar terceiro endpoint inserindo um novo registro e usar o protocolo http.
7 - Criar quarto endpoint deletando um novo registro e usar o protocolo http.
8 - Utilize a conexão com o banco de dados para fazer as operações CRUD