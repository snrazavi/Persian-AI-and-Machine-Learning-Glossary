"""This is the main application file for the Persian-English glossary web app."""
from flask import Flask
from models.glossary_term import db
from config import Config
from views.routes import main
from views.auth_utils import login_manager


def create_app(config_class=Config):
    """Create a Flask application"""
    app = Flask(__name__)
    app.secret_key = config_class.SECRET_KEY  # flask.session requires a secret key
    app.config.from_object(config_class)      # load config from config.py
    db.init_app(app)                          # initialize database and bind it to the app
    app.register_blueprint(main)              # register the main blueprint
    return app


application = create_app(Config)
login_manager.login_view = "main.login"
login_manager.init_app(application)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
