import os
import yaml
import difflib
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

from glossary import Glossary
from helpers import generate_star_rating

load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


glossary = Glossary(dictionary_file="Glossary_for_ratings.yaml")


@app.route("/", methods=["GET", "POST"])
def index():
    """Home page"""
    if request.method == "POST":
        if "search-term" in request.form:
            term = request.form.get("search-term")
            translations = glossary.search_dictionary(term)

            if translations is None:
                # find the closest match to the term
                closest_match = difflib.get_close_matches(term, glossary.dictionary.keys(), n=1, cutoff=0.6)
                if closest_match:
                    similar_term = closest_match[0]
                    translations = glossary.search_dictionary(similar_term)
                    return render_template(
                        "index.html", generate_star_rating=generate_star_rating,
                        translations=translations, term=similar_term, original_term=term)
                else:
                    return render_template("index.html", not_found=True, term=term)
            else:
                return render_template(
                    "index.html", generate_star_rating=generate_star_rating, 
                    translations=translations, term=term)
        elif "new-english-term" in request.form and "new-persian-translation" in request.form:
            english_term = request.form.get("new-english-term")
            persian_translation = request.form.get("new-persian-translation")

            if glossary.add_translation(english_term, persian_translation):
                flash("Thank you for your contribution! Your suggestion will be added to the dictionary after approval.")
            else:
                flash("This translation alreadys exists in the dictionary!")
            return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/rate_translation", methods=["POST"])
def rate_translation():
    """Rate a translation"""
    english_term = request.form.get("term")
    translation_index = request.form.get("translation_index")
    new_rating = int(request.form.get("new_rating"))

    if new_rating is not None and new_rating in range(1, 6):
        glossary.update_rating(english_term, translation_index, new_rating)
        flash("Thank you for your rating!")
    else:
        flash("Please select a rating in range 1-5!")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
