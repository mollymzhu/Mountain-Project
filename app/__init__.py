from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
# initialize Flask Admin
admin = Admin(app, name='Site Administration', template_mode='bootstrap3')

# give the app access to the bootstrap css/js
bootstrap = Bootstrap(app)

# set up the login manager
loginmanager = LoginManager()
loginmanager.init_app(app)

# point the app to the login page if an unauthenticated
# user tried to access a login_required page
loginmanager.login_view = "login"

from app import views
