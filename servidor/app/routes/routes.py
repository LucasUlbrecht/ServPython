from flask import Blueprint, jsonify, render_template, redirect, request, url_for
from flask_login import login_required, current_user, logout_user
from app.models.models import db, UserAdmin
from flask_httpauth import HTTPBasicAuth
import datetime
import jwt
import os

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = UserAdmin.query.filter_by(user_id=username).first()
    if user and user.check_password(password):
        return user
    return None

# Importando as interfaces para operações de dados
from app.models.queries import add_product_interface, get_all_users_interface, get_products_interface

routes = Blueprint('routes', __name__)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY', 'default_secret'), algorithm='HS256')
    return token


# Rota para listar produtos
@routes.route('/products', methods=['GET'])
@login_required
def get_products():
    # A lógica para listar produtos vai aqui
    return jsonify({"products": []})  # Exemplo de resposta

# Rota de logout
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))  # Redireciona para a página inicial após o logout

# Rota para listar usuários (requisição autenticada)
@routes.route('/users', methods=['GET'])
@login_required
def get_users():
    users = get_all_users_interface()  # Utiliza a interface para obter os usuários
    return jsonify({"users": users})
    

# Rota para adicionar um produto
@routes.route('/add_product', methods=['POST'])
@login_required
def add_product_route():
    data = request.json  # Obtém os dados do corpo da requisição

    # Valida se os campos necessários foram fornecidos
    barcode = data.get('barcode')
    product_name = data.get('product_name')
    user_id = data.get('user_id')

    if not barcode or not product_name or not user_id:
        return jsonify({"status": "fail", "message": "Todos os campos são obrigatórios!"}), 400  # Retorna erro se algum campo estiver faltando

    # Chama a interface para adicionar o produto
    response, status_code = add_product_interface(barcode, product_name, user_id)

    # Retorna a resposta com o status apropriado
    return jsonify(response), status_code


# Rota para obter produtos de um cliente
@routes.route('/products/<user_id>', methods=['GET'])
@login_required
def get_products_user(user_id):
    products = get_products_interface(user_id)  # Utiliza a interface para obter os produtos do cliente
    return jsonify({"products": products})

# Rota para cadastro de novo usuário
@routes.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Nome de usuário e senha são obrigatórios!"}), 400

    # Verifica se o usuário já existe
    existing_user = UserAdmin.query.filter_by(user_id=username).first()
    if existing_user:
        return jsonify({"status": "fail", "message": "Usuário já existe!"}), 400

    # Cria um novo usuário
    new_user = UserAdmin(user_id=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "Usuário cadastrado com sucesso!"}), 200
@routes.route('/admin_dashboard')
@auth.login_required  # Usando Basic Auth
def admin_dashboard():
    return render_template('admin_dashboard.html')  # Página principal do admin
