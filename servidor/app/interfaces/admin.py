from flask import Flask, Response, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models.models import ClientProduct, db, UserAdmin, Client, Product
from flask_login import login_user

# Código para login do usuário admin
def login_admin():
    admin = UserAdmin.query.filter_by(user_id='admin').first()
    if admin:
        login_user(admin)

auth = HTTPBasicAuth()  # Inicializa o auth para autenticação básica

# admin.py (Interface de administração)
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app.models.models import db, UserAdmin, Client, Product, ClientProduct
from app.models.db_operations import validate_authentication
from werkzeug.exceptions import HTTPException

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

def setup_admin(app):
    admin = Admin(app, name='Admin', template_mode='bootstrap3')

    # Classe ModelView personalizada para proteger o acesso
    class AdminModelView(ModelView):
        def is_accessible(self):
            auth_data = auth.get_auth()
            if auth_data:
                username = auth_data['username']
                password = auth_data['password']
                return validate_authentication(username, password) and username in app.config.get('ADMINISTRATORS', [])
            raise AuthException('Not authenticated.')

        def _handle_view(self, name):
            if not self.is_accessible():
                return redirect(url_for("security.login"))
        def _display_roles(self, context, model, name):
            return ", ".join([role.name.capitalize() for role in model.roles])
        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for("security.login"))

    # Adicionando as views
    admin.add_view(AdminModelView(UserAdmin, db.session, category='Gestão de Usuários'))
    admin.add_view(AdminModelView(Client, db.session, category='Gestão de Clientes'))
    admin.add_view(AdminModelView(Product, db.session, category='Gestão de Produtos'))
    admin.add_view(AdminModelView(ClientProduct, db.session, category='Gestão de Relacionamentos'))
