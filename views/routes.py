"""This module contains the main blueprint for the application."""
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash)

from views.helpers import (
    generate_star_rating,
    search_glossary_term,
    submit_new_translation,
    update_translation_rating)

from models.glossary_term import GlossaryTerm


main = Blueprint("main", __name__)


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
