from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy()


class UserAdmin(db.Model, UserMixin):
    user_id = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)  # Para armazenar o hash da senha

    # Definindo o método para armazenar a senha
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Método para verificar a senha
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Tabela para Clients (Clientes)
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)

    # Relacionamento com o modelo de produtos
    products = db.relationship('Product', secondary='client_product', backref='clients')

# Tabela para Produtos
class Product(db.Model):
    barcode = db.Column(db.String(80), primary_key=True)
    product_name = db.Column(db.String(120), nullable=False)

# Tabela de junção entre Cliente e Produto (M:N)
class ClientProduct(db.Model):
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    product_barcode = db.Column(db.String(80), db.ForeignKey('product.barcode'), primary_key=True)

def populate_db():
    # Dados do usuário admin
    admin_user_id = 'admin'
    admin_password = 'admin123'

    # Verifique se o admin já existe
    admin = UserAdmin.query.filter_by(user_id=admin_user_id).first()
    if not admin:
        # Se não existir, crie o usuário admin
        admin = UserAdmin(user_id=admin_user_id)
        admin.set_password(admin_password)
        db.session.add(admin)

    # Dados dos clientes
    clients_data = [
        ('client1', 'Cliente 1', 'cliente1@example.com'),
        ('client2', 'Cliente 2', 'cliente2@example.com'),
        ('client3', 'Cliente 3', 'cliente3@example.com')
    ]
    
    # Adicionar clientes se não existirem
    for user_id, name, email in clients_data:
        existing_client = Client.query.filter_by(email=email).first()
        if not existing_client:
            client = Client(user_id=user_id, name=name, email=email)
            db.session.add(client)
    
    # Dados dos produtos
    products_data = [
        ('123456789', 'Produto 1'),
        ('987654321', 'Produto 2'),
        ('456789123', 'Produto 3')
    ]
    
    # Adicionar produtos se não existirem
    for barcode, product_name in products_data:
        existing_product = Product.query.filter_by(barcode=barcode).first()
        if not existing_product:
            product = Product(barcode=barcode, product_name=product_name)
            db.session.add(product)

    # Relacionar clientes com produtos
    client1 = Client.query.filter_by(user_id='client1').first()
    client2 = Client.query.filter_by(user_id='client2').first()
    client3 = Client.query.filter_by(user_id='client3').first()

    product1 = Product.query.filter_by(barcode='123456789').first()
    product2 = Product.query.filter_by(barcode='987654321').first()
    product3 = Product.query.filter_by(barcode='456789123').first()

    # Função para verificar e adicionar a relação client-product
    def add_client_product_relation(client, product):
        if client and product:
            # Verificar se o relacionamento já existe
            existing_relation = db.session.query(ClientProduct).filter_by(client_id=client.id, product_barcode=product.barcode).first()
            if not existing_relation:
                client.products.append(product)
                db.session.commit()  # Comitar após cada relação adicionada

    # Relacionando clientes aos produtos, se não existirem
    add_client_product_relation(client1, product1)
    add_client_product_relation(client2, product2)
    add_client_product_relation(client3, product3)

    # Commit para salvar todas as alterações no banco de dados
    db.session.commit()
