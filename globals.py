from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def init():
    global master_servers;
    master_servers = {}
