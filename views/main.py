"""This module contains the main blueprint for the application."""
import difflib
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from models.glossary_term import GlossaryTerm, db
from models.translation import Translation
from helpers import generate_star_rating

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
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


@main.route("/rate_translation", methods=["POST"])
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
