from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from app.models.models import db, UserAdmin, populate_db
from app. models.db_operations import create_database
from app.models.queries import get_all_users_interface,  get_all_admin_interface
from flask_migrate import Migrate
import os
from app.config import Config
from flask_httpauth import HTTPBasicAuth

# Inicializa a extensão SQLAlchemy e Flask-Login
login_manager = LoginManager()

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = UserAdmin.query.filter_by(user_id=username).first()
    if user and user.check_password(password):
        return user
    return None

@login_manager.user_loader
def load_user(user_id):
    return UserAdmin.query.get(user_id)

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados com SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI  # Caminho para o seu banco de dados
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    
    # Chave secreta dinâmica para segurança
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    app.config['BASIC_AUTH_FORCE'] = Config.BASICAUTHFORCE


    # Inicializa o banco de dados e login
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
        populate_db()
        
        print(get_all_users_interface())
        print(get_all_admin_interface())
    
    # Configura a migração do banco de dados
    migrate = Migrate(app, db)

    
    # Inicializa a interface de admin
    from app.interfaces.admin import setup_admin
    setup_admin(app)
    
    return app
