import sqlite3

DB_NAME = 'database.db'

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            barcode TEXT,
            product_name TEXT,
            user_id TEXT,
            PRIMARY KEY (barcode, user_id),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()

def find_product_by_barcode(barcode, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT product_name FROM products 
        WHERE barcode = ? AND user_id = ?
    ''', (barcode, user_id))
    
    product = cursor.fetchone()
    conn.close()
    
    return product

def add_product(barcode, product_name, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO products (barcode, product_name, user_id) 
        VALUES (?, ?, ?)
    ''', (barcode, product_name, user_id))
    
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users')
    users = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return users

def user_exists(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    return user is not None


def get_user_products(user_id):
    conn = sqlite3.connect('database.db')  # Assumindo que você está usando SQLite
    cursor = conn.cursor()
    
    cursor.execute("SELECT barcode, product_name FROM products WHERE user_id = ?", (user_id,))
    products = cursor.fetchall()
    
    conn.close()
    return [{"barcode": row[0], "product_name": row[1]} for row in products]



def add_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Caso o usuário já exista, simplesmente ignora o erro
    finally:
        conn.close()

    return products
