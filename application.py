"""This is the main application file for the Persian-English glossary web app."""
import difflib
import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_sqlalchemy import SQLAlchemy
from glossary import Glossary
from helpers import generate_star_rating

# load RDS credentials from environment variables
RDS_USERNAME = os.environ.get('RDS_USERNAME')
RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
RDS_ENDPOINT = os.environ.get('RDS_ENDPOINT')
RDS_PORT = os.environ.get('RDS_PORT')
RDS_DB_NAME = os.environ.get('RDS_DB_NAME')

application = Flask(__name__)
application.secret_key = "my_unique_secret_key"  # os.environ.get("SECRET_KEY")
# application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///glossary.db"
application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_ENDPOINT}:{RDS_PORT}/{RDS_DB_NAME}"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(application)


# read access key and secret access key from environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

class GlossaryTerm(db.Model):
    """A class for the glossary terms"""
    id = db.Column(db.Integer, primary_key=True)
    english_term = db.Column(db.String(200), nullable=False)
    translations = db.relationship("Translation", backref="glossary_term", lazy=True)

    def __repr__(self):
        return f"<GlossaryTerm {self.english_term}>"


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


@application.route("/", methods=["GET", "POST"])
def index():
    """Home page"""
    if request.method == "POST":
        if "search-term" in request.form:
            term = request.form.get("search-term")
            term = term.strip().lower()
            term_entry = GlossaryTerm.query.filter_by(english_term=term).first()
            if term_entry:
                translations = term_entry.translations
                return render_template(
                    "index.html", generate_star_rating=generate_star_rating, 
                    translations=translations, term=term)
            
            # search for the closest match to the term
            all_terms = [glossary_term.english_term for glossary_term in GlossaryTerm.query.all()]
            closest_match = difflib.get_close_matches(term, all_terms, n=1, cutoff=0.6)
            if closest_match:
                similar_term = closest_match[0]
                translations = GlossaryTerm.query.filter_by(english_term=similar_term).first().translations
                return render_template(
                    "index.html", generate_star_rating=generate_star_rating,
                    translations=translations, term=similar_term, original_term=term)
            
            # no match found
            return render_template("index.html", not_found=True, term=term)
                
        if "new-english-term" in request.form and "new-persian-translation" in request.form:
            english_term = request.form.get("new-english-term")
            persian_translation = request.form.get("new-persian-translation")

            # cherck the translation and the term are not empty
            if not english_term or not persian_translation:
                flash("Please enter a valid term and translation!")
                return redirect(url_for("index"))

            term_entry = GlossaryTerm.query.filter_by(english_term=english_term).first()

            # check if the translation already exists in the dictionary
            translation_entry = Translation.query.filter_by(persian_translation=persian_translation).first()
            if translation_entry:
                flash("This translation already exists in the dictionary!")
                return redirect(url_for("index"))
            else:
                if term_entry:
                    glossary_term_id = term_entry.id
                else:
                    new_glossary_term = GlossaryTerm(english_term=english_term)
                    db.session.add(new_glossary_term)
                    db.session.commit()
                    db.session.flush() # to get the id of the new glossary term
                    glossary_term_id = new_glossary_term.id

                new_translation = Translation(
                    persian_translation=persian_translation, glossary_term_id=glossary_term_id)
                db.session.add(new_translation)
                db.session.commit()
                flash("Thank you for your contribution!\
                      Your suggestion will be added to the dictionary after approval.")
                return redirect(url_for("index"))

    return render_template("index.html")

@application.route("/rate_translation", methods=["POST"])
def rate_translation():
    """Rate a translation"""
    english_term = request.form.get("term")
    translation_index = request.form.get("translation_index")

    term_entry = GlossaryTerm.query.filter_by(english_term=english_term).first()

    if term_entry:
        translations = term_entry.translations
        translation = translations[int(translation_index)]
        translation.rating_no += 1
        db.session.commit()

        new_rating = int(request.form.get("new_rating"))

        if new_rating is not None and new_rating in range(0, 6):
            translation.rating = (translation.rating * translation.rating + new_rating) / (translation.rating_no + 1)
            # round the rating to the nearest 0.5
            translation.rating = round(translation.rating * 2) / 2
            db.session.commit()
            # glossary.update_rating(english_term, translation_index, new_rating)
            flash("Thank you for your rating!")
        else:
            flash("Please select a rating in range 1-5!")

        return redirect(url_for("index"))


if __name__ == "__main__":
    # with application.app_context():
    #     db.create_all()
    application.run(host="0.0.0.0", port=80)
