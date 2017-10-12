import os
from getpass import getuser, getpass
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'l17zXzkSmb

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
    'local': SQLALCHEMY_DATABASE_URI
}
BOOTSTRAP_SERVE_LOCAL = True
