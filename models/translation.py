"""A module for the translation of the glossary terms"""
from models.glossary_term import db


class Translation(db.Model):
    """A class for the translations of the glossary terms"""
    id = db.Column(db.Integer, primary_key=True)
    persian_translation = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    rating_no = db.Column(db.Integer, nullable=False, default=0)
    approved = db.Column(db.Boolean, nullable=False, default=True)
    glossary_term_id = db.Column(db.Integer, db.ForeignKey("glossary_term.id"), nullable=False)

    def __repr__(self):
        return f"<Translation {self.persian_translation}>"
