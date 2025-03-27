
Rota	Método	Porta Interna	Porta Externa Recomendada	Descrição

/users	GET	5000	443 (HTTPS)	Lista todos os usuários

/barcode	POST	5000	443 (HTTPS)	Consulta produto por código de barras

/add_product	POST	5000	443 (HTTPS)	Adiciona novo produto

/products/<user_id>	GET	5000	443 (HTTPS)	Lista produtos de um usuário específico


----------


1. Tabela users
Coluna	Tipo	Descrição	Restrições
user_id	TEXT	Identificador único do usuário	PRIMARY KEY
Operações:

add_user(user_id): Adiciona novo usuário (ignora se já existir)

user_exists(user_id): Verifica se usuário existe

get_all_users(): Lista todos os IDs de usuários

2. Tabela products
Coluna	Tipo	Descrição	Restrições
barcode	TEXT	Código de barras do produto	PRIMARY KEY (composta com user_id)
product_name	TEXT	Nome do produto	NOT NULL
user_id	TEXT	Dono do produto	FOREIGN KEY (users.user_id)
Operações:

add_product(barcode, product_name, user_id): Cadastra novo produto

find_product_by_barcode(barcode, user_id): Busca produto por código

get_user_products(user_id): Lista todos produtos de um usuário
