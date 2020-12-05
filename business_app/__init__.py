from flask import Flask
from .config import sql_config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

global db
global jwt


def create_app():
    """ to create and configure the flask application."""
    try:
        app = Flask(__name__, instance_relative_config=True)
        CORS(app)
        app.config.from_object(sql_config.Config)
        global db
        global jwt
        db = SQLAlchemy(app)
        app.config['JWT_SECRET_KEY'] = 'super-secret&*(%3'
        jwt = JWTManager(app)
        from .views import (user, roles, operations, login, download_reports)

        # app.register_blueprint(user.bp)
        app.register_blueprint(operations.bp)
        app.register_blueprint(login.bp)
        app.register_blueprint(download_reports.bp)

        @app.route("/")
        def home():
            return """<h1> Welcome to  Service </h1>"""

        @app.teardown_request
        def session_clear(exception=None):
            db.session.remove()
            if exception and db.session.is_active:
                db.session.rollback()

        return app
    except Exception as err:
        print('Error in service create_app :' + str(err))
