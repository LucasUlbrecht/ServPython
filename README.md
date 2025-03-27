
Rota	Método	Porta Interna	Porta Externa Recomendada	Descrição

/users	GET	5000	443 (HTTPS)	Lista todos os usuários

/barcode	POST	5000	443 (HTTPS)	Consulta produto por código de barras

/add_product	POST	5000	443 (HTTPS)	Adiciona novo produto

/products/<user_id>	GET	5000	443 (HTTPS)	Lista produtos de um usuário específico
