from app.models.db_operations import get_all_admin, get_all_users, add_product, get_user_products, find_product_by_barcode

# Interface para consultar todos os usuários
def get_all_users_interface():
    users = get_all_users()  # Função para obter todos os usuários
    return [{"user_id": user.user_id, "username": user.name} for user in users]
def get_all_admin_interface():
    admins = get_all_admin()
    return [{"admin_id": admin.user_id, "password": admin.password_hash} for admin in admins]

# Interface para adicionar um novo produto
def add_product_interface(barcode, product_name, user_id):
    if not barcode or not product_name or not user_id:
        return {"status": "fail", "message": "Dados inválidos."}, 400

    try:
        add_product(barcode, product_name, user_id)  # Função que adiciona o produto
        return {"status": "success", "message": f"Produto {product_name} adicionado com sucesso!"}, 200
    except Exception as e:
        return {"status": "fail", "message": str(e)}, 400

# Interface para obter produtos de um cliente
def get_products_interface(user_id):
    products = get_user_products(user_id)  # Função que busca os produtos do cliente
    return [{"barcode": product.barcode, "product_name": product.product_name} for product in products]

# Função para verificar se o produto já existe
def product_exists(barcode, user_id):
    return find_product_by_barcode(barcode, user_id) is not None
