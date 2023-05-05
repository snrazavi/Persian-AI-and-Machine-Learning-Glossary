"""This module contains the GlossaryTerm class."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class GlossaryTerm(db.Model):
    """A class for the glossary terms"""
    id = db.Column(db.Integer, primary_key=True)
    english_term = db.Column(db.String(200), nullable=False)
    translations = db.relationship("Translation", backref="glossary_term", lazy=True)

    def __repr__(self):
        return f"<GlossaryTerm {self.english_term}>"
