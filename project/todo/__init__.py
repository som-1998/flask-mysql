from flask import Blueprint

database_bp = Blueprint("database_bp", __name__ , template_folder='templates')

from .routes import *