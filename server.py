from flask import Flask, request, jsonify
from flask_cors import CORS
from db_operations import create_database, find_product_by_barcode, add_product, get_all_users, user_exists, add_user

app = Flask(__name__)
CORS(app)

# Inicializa o banco de dados (cria as tabelas globais)
create_database()

@app.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify({"users": users})

@app.route('/barcode', methods=['POST'])
def barcode():
    data = request.json
    barcode = data.get('barcode')
    user_id = data.get('userId')

    if not user_id or not barcode:
        return jsonify({"status": "fail", "message": "Dados inválidos."}), 400

    # Verifica se o usuário existe, se não, cadastra um novo usuário
    if not user_exists(user_id):
        add_user(user_id)

    # Verifica se o código de barras está na tabela do usuário
    product = find_product_by_barcode(barcode, user_id)

    if product:
        # Produto encontrado
        return jsonify({"status": "success", "message": f"Produto encontrado: {product[0]}"}), 200
    else:
        # Produto não encontrado, solicita o nome do produto
        return jsonify({"status": "not_found", "message": "Produto não encontrado. Envie o nome do produto."}), 404

@app.route('/add_product', methods=['POST'])
def add_product_route():
    data = request.json
    barcode = data.get('barcode')
    product_name = data.get('product_name')
    user_id = data.get('userId')

    if not user_id or not barcode or not product_name:
        return jsonify({"status": "fail", "message": "Dados inválidos."}), 400

    try:
        # Adiciona o produto na tabela do usuário
        add_product(barcode, product_name, user_id)
        return jsonify({"status": "success", "message": f"Produto {product_name} cadastrado com sucesso!"}), 200
    except sqlite3.IntegrityError:
        # Caso o código de barras já exista no banco de dados do usuário
        return jsonify({"status": "fail", "message": "Este código de barras já está cadastrado."}), 400

@app.route('/products/<user_id>', methods=['GET'])
def get_products(user_id):
    products = get_user_products(user_id)
    return jsonify({"products": products})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
