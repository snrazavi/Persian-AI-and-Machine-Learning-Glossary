"""This is the main application file for the Persian-English glossary web app."""
from flask import Flask
from models.glossary_term import db
from views.main import main
from config import Config


def create_app(config_class=Config):
    """Create a Flask application"""
    app = Flask(__name__)
    app.secret_key = config_class.SECRET_KEY  # flask.session requires a secret key
    app.config.from_object(config_class)      # load config from config.py
    db.init_app(app)                          # initialize database and bind it to the app
    app.register_blueprint(main)              # register the main blueprint
    return app


application = create_app(Config)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
