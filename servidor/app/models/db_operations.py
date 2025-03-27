from app.models.models import Client, db, UserAdmin, Product
from werkzeug.security import generate_password_hash, check_password_hash


# Função para inicializar o banco de dados e criar as tabelas
def create_database():
    db.create_all()

# Função para verificar se o usuário existe
def user_exists(user_id):
    return Client.query.filter_by(user_id=user_id).first() is not None

# Função para adicionar um novo usuário
def add_user(user_id, username):
    # Aqui você pode gerar uma senha padrão ou gerar uma senha aleatória
    user = Client(user_id=user_id, username=username)
    db.session.add(user)
    db.session.commit()

# Função para procurar um produto pelo código de barras
def find_product_by_barcode(barcode, user_id):
    return Product.query.filter_by(barcode=barcode, user_id=user_id).first()

# Função para adicionar um produto
def add_product(barcode, product_name, user_id):
    if not user_exists(user_id):  # Verifica se o usuário já existe
        add_user(user_id, user_id)  # Se o usuário não existir, cria um novo usuário

    # Criação do objeto Produto e adição ao banco
    product = Product(barcode=barcode, product_name=product_name, user_id=user_id)
    db.session.add(product)
    db.session.commit()  # Persiste as mudanças no banco de dados


# Função para listar todos os usuários
def get_all_users():
    return Client.query.all()

def get_all_admin():
    return UserAdmin.query.all()

# Função para listar os produtos de um cliente
def get_user_products(user_id):
    return Product.query.filter_by(user_id=user_id).all()
def validate_authentication(user_id, password):
    """
    Valida o login do usuário pelo nome de usuário e senha.
    
    :param username: Nome de usuário fornecido.
    :param password: Senha fornecida.
    :return: True se as credenciais forem válidas, False caso contrário.
    """
    # Busca o usuário no banco de dados
    user = UserAdmin.query.filter_by(user_id).first()
    
    if user:
        # Compara a senha fornecida com a senha armazenada
        return check_password_hash(user.password, password)
    
    return False