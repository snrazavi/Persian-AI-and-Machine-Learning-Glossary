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


def search_glossary_term(glossary_term: str):
    """ Search the database for the given term.
    If the term is found, return the translations.
    If the term is not found, search for the closest match and return its translations.
    If no match is found, return None.

    :param glossary_term: the term to search for
    :type glossary_term: str
    :return: the translations of the term
    """
    term_entry = GlossaryTerm.query.filter_by(english_term=glossary_term).first()
    if term_entry:
        return sorted(enumerate(term_entry.translations), key=lambda t: t[1].rating, reverse=True)

    # search for the closest match to the term
    all_terms = [glossary_term.english_term for glossary_term in GlossaryTerm.query.all()]
    closest_match = difflib.get_close_matches(glossary_term, all_terms, n=1, cutoff=0.6)
    if closest_match:
        similar_term = closest_match[0]
        translations = GlossaryTerm.query.filter_by(english_term=similar_term).first().translations
        return sorted(enumerate(translations), key=lambda t: t[1].rating, reverse=True), similar_term

    # no match found
    return None


def submit_new_translation(english_term: str, persian_translation: str):
    """Submit a new translation to the database.

    :param english_term: the English term
    :type english_term: str
    :param persian_translation: the Persian translation
    :type persian_translation: str
    """
    term_entry = GlossaryTerm.query.filter_by(english_term=english_term).first()
    translation_entry = Translation.query.filter_by(persian_translation=persian_translation).first()

    if translation_entry:
        return False

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
    return True


def update_translation_rating(term_entry, original_index, new_rating):
    """Update the rating of a translation.

    :param translation: the translation to update
    :type translation: Translation
    :param original_index: the index of the translation in the list of translations
    :type original_index: int
    :param new_rating: the new rating
    :type new_rating: int
    """
    translation = term_entry.translations[int(original_index)]
    updated_rating = (translation.rating * translation.rating_no + new_rating) / (translation.rating_no + 1)

    # round the rating to the nearest 0.5
    translation.rating = round(updated_rating * 2) / 2
    db.session.commit()

    translation.rating_no += 1
    db.session.commit()


@main.route("/", methods=["GET", "POST"])
def index():
    """Home page"""
    if request.method == "POST":
        if "search-term" in request.form:
            term = request.form.get("search-term").strip().lower()
            result = search_glossary_term(term)

            if result:
                if isinstance(result, tuple):
                    translations, similar_term = result
                    return render_template(
                        "index.html", generate_star_rating=generate_star_rating,
                        translations=translations, term=similar_term, original_term=term)

                translations = result
                return render_template(
                    "index.html", generate_star_rating=generate_star_rating,
                    translations=translations, term=term)

            return render_template("index.html", not_found=True, term=term)

        if "new-english-term" in request.form and "new-persian-translation" in request.form:
            english_term = request.form.get("new-english-term").strip().lower()
            persian_translation = request.form.get("new-persian-translation").strip()

            # cherck the translation and the term are not empty
            if not english_term or not persian_translation:
                flash("Please enter a valid term and translation!")
                return redirect(url_for("main.index"))

            if submit_new_translation(english_term, persian_translation):
                flash("Thank you for your contribution!\
                      Your suggestion will be added to the dictionary after approval.")
            else:
                flash("This translation already exists in the dictionary!")
            return redirect(url_for("main.index"))

    return render_template("index.html")


@main.route("/rate_translation", methods=["POST"])
def rate_translation():
    """Rate a translation"""
    english_term = request.form.get("term").strip().lower()
    translation_index = request.form.get("original_index")
    new_rating = int(request.form.get("new_rating"))

    if new_rating is None or new_rating not in range(0, 6):
        flash("Please select a rating in range 0-5!")
        return redirect(url_for("main.index"))

    term_entry = GlossaryTerm.query.filter_by(english_term=english_term).first()
    update_translation_rating(term_entry, translation_index, new_rating)
    flash("Thank you for your feedback!")

    return redirect(url_for("main.index"))
