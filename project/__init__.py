from flask import Flask , redirect, url_for
from .config import Config
from .db import mysql
from .todo import database_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    app.register_blueprint(database_bp, url_prefix='/students')

    @app.route("/")
    def home_page():
        return redirect(url_for("database_bp.students_page"))

    return app