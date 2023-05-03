import os
import yaml
import difflib
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


def load_dictionary():
    """Load the dictionary from a YAML file"""
    with open("Glossary_for_ratings.yaml", "r", encoding="utf-8") as file:
        dictionary = yaml.safe_load(file)

    # convert the list of dictionaries to a dictionary
    # dictionary = {entry['english'].lower(): entry['persian'] for entry in dictionary}
    # dictionary = {entry['english'].lower(): entry['translations'] for entry in dictionary}

    # sort the dictionary for each term based on the rating
    for term in dictionary:
        dictionary[term] = sorted(dictionary[term], key=lambda x: x['rating'], reverse=True)

    return dictionary


def save_dictionary(dictionary):
    """Save the dictionary to a YAML file"""
    with open("Glossary_for_ratings.yaml", "w", encoding="utf-8") as file:
        yaml.dump(dictionary, file, allow_unicode=True)


def search_dictionary(term):
    """Search the dictionary for a term"""
    term = term.lower()
    return dictionary.get(term)
    # # search for a term in a list of dictionaries
    # for entry in dictionary:
    #     if entry['english'].lower() == term:
    #         return entry['persian']
    # return None
    # translations = dictionary.get(term.lower())
    # if translations is None:
    #     # find the closest match to the term
    #     closest_match = difflib.get_close_matches(term, dictionary.keys(), n=1, cutoff=0.6)
    #     if closest_match:
    #         closest_match = closest_match[0]
    #         return render_template("index.html", translations=translations, term=similar_term, original_term=term)
    #     else:
    #         return render_template("index.html", not_found=True, term=term)
    # else:
    #     return render_template("index.html", translations=translations, term=term)


dictionary = load_dictionary()

@app.route("/", methods=["GET", "POST"])
def index():
    """Home page"""
    if request.method == "POST":
        if "search-term" in request.form:
            term = request.form.get("search-term")
            # translations = search_dictionary(term)
            translations = dictionary.get(term.lower())
            if translations is None:
                # find the closest match to the term
                closest_match = difflib.get_close_matches(term, dictionary.keys(), n=1, cutoff=0.6)
                if closest_match:
                    similar_term = closest_match[0]
                    print(f"Most similar term: {similar_term}")
                    translations = dictionary.get(similar_term)
                    translations = [translation for translation in translations 
                                    if translation.get('approved', True)]
                    return render_template(
                        "index.html", translations=translations, 
                        term=similar_term, original_term=term)
                else:
                    return render_template("index.html", not_found=True, term=term)
            else:
                translations = [translation for translation in translations 
                                if translation.get('approved', True)]
                return render_template("index.html", translations=translations, term=term)
        elif "new-english-term" in request.form and "new-persian-translation" in request.form:
            english_term = request.form.get("new-english-term")
            persian_translation = request.form.get("new-persian-translation")
            new_entry = {"persian": persian_translation, "rating": 0, 'approved': False}
            # check if the persian translation already exists in the dictionary
            for entry in dictionary.get(english_term.lower(), []):
                if entry["persian"] == persian_translation:
                    flash("This translation already exists in the dictionary!")
                    return redirect(url_for("index"))
            if english_term.lower() in dictionary:
                dictionary[english_term.lower()].append(new_entry)
            else:
                dictionary[english_term.lower()] = [new_entry]
            save_dictionary(dictionary)
            flash("Thank you for your contribution! Your suggestion will be added to the dictionary after approval.")
            return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/rate_translation", methods=["POST"])
def rate_translation():
    """Rate a translation"""
    english_term = request.form.get("english-term")
    persian_translation = request.form.get("persian-translation")
    rating = int(request.form.get("rating"))

    translations = dictionary.get(english_term.lower())
    if translations:
        for translation_entry in translations:
            if translation_entry["persian"] == persian_translation:
                if "rating_no" not in translation_entry:
                    translation_entry["rating_no"] = 0
                translation_entry["rating_no"] += 1
                # compute the new rating by a weighted average
                rating = (translation_entry["rating_no"] * translation_entry["rating"] + rating) / (translation_entry["rating_no"] + 1)
                # round the rating to the nearest 0.5#
                rating = round(rating * 2) / 2
                translation_entry["rating"] = rating
                print(f"Rating for {english_term} - {persian_translation} updated to {rating}")
                # sort the translations based on the rating
                translations = sorted(translations, key=lambda x: x['rating'], reverse=True)
                # update the dictionary
                dictionary[english_term.lower()] = translations
                break
        save_dictionary(dictionary)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
