"""This is the main application file for the Persian-English glossary web app."""
from flask import Flask
from models.glossary_term import db
from views.main import main
from config import Config


def create_app(config_class=Config):
    """Create and configure the Flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    app.register_blueprint(main)

    return app


application = create_app()


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
