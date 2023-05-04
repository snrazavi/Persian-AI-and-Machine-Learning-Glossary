"""This is the main application file for the Persian-English glossary web app."""
import boto3
import difflib
import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

import openai

from glossary import Glossary
from helpers import generate_star_rating

load_dotenv()


application = Flask(__name__)
application.secret_key = "my_unique_secret_key"  # os.environ.get("SECRET_KEY")

# read access key and secret access key from environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


s3 = boto3.client(service_name='s3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name='us-west-2')

bucket_name = 'snrazavi'
glossary_file_key = 'Glossary_for_ratings.yaml'
GENERATE_DESCRIPTION = False

glossary = Glossary("Glossary_for_ratings.yaml", s3, bucket_name, glossary_file_key)

def generate_description(term):
    prompt = f"Write a brief description of the term '{term}' in the\
               context of AI and Machine Learning in Persian language.\
               Possibly provide a few links to learn more about the query"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.6,
    )

    return response.choices[0].text.strip()


@application.route("/", methods=["GET", "POST"])
def index():
    """Home page"""
    if request.method == "POST":
        if "search-term" in request.form:
            term = request.form.get("search-term")
            translations = glossary.search_dictionary(term)

            if translations is None:
                # find the closest match to the term
                closest_match = difflib.get_close_matches(
                    term, glossary.dictionary.keys(), n=1, cutoff=0.6)
                if closest_match:
                    similar_term = closest_match[0]
                    translations = glossary.search_dictionary(similar_term)
                    return render_template(
                        "index.html", generate_star_rating=generate_star_rating,
                        translations=translations, term=similar_term, original_term=term)
                else:
                    return render_template("index.html", not_found=True, term=term)
            else:
                if GENERATE_DESCRIPTION:
                    description = generate_description(term)
                    return render_template(
                        "index.html", generate_star_rating=generate_star_rating, 
                        translations=translations, term=term, description=description)
                else:
                    return render_template(
                        "index.html", generate_star_rating=generate_star_rating, 
                        translations=translations, term=term)

        elif "new-english-term" in request.form and "new-persian-translation" in request.form:
            english_term = request.form.get("new-english-term")
            persian_translation = request.form.get("new-persian-translation")

            if glossary.add_translation(english_term, persian_translation):
                flash("Thank you for your contribution!\
                      Your suggestion will be added to the dictionary after approval.")
            else:
                flash("This translation alreadys exists in the dictionary or it is not valid!")
            return redirect(url_for("index"))
    return render_template("index.html")

@application.route("/rate_translation", methods=["POST"])
def rate_translation():
    """Rate a translation"""
    english_term = request.form.get("term")
    translation_index = request.form.get("translation_index")
    new_rating = int(request.form.get("new_rating"))

    if new_rating is not None and new_rating in range(0, 6):
        glossary.update_rating(english_term, translation_index, new_rating)
        flash("Thank you for your rating!")
    else:
        flash("Please select a rating in range 1-5!")

    return redirect(url_for("index"))


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
