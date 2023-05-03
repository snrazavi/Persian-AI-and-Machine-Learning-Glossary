"""This module contains functions for loading, saving, searching, and adding to the dictionary."""
import yaml


def load_dictionary():
    """Load the dictionary from a YAML file"""
    with open("Glossary_for_ratings.yaml", "r", encoding="utf-8") as file:
        dictionary = yaml.safe_load(file)

    # sort the dictionary for each term based on the rating
    for term in dictionary:
        dictionary[term] = sorted(dictionary[term], key=lambda x: x['rating'], reverse=True)

    return dictionary


dictionary = load_dictionary()


def save_dictionary(dictionary):
    """Save the dictionary to a YAML file"""
    with open("Glossary_for_ratings.yaml", "w", encoding="utf-8") as file:
        yaml.dump(dictionary, file, allow_unicode=True)


def search_dictionary(term):
    term = term.lower()
    translations = dictionary.get(term)
    if translations is None:
        return None
    return [translation for translation in translations if translation.get("approved", True)]


def add_translation(english_term, persian_translation):
    english_term = english_term.lower()
    new_entry = {"persian": persian_translation, "rating": 0, "approved": False}
    
    for entry in dictionary.get(english_term, []):
        if entry["persian"] == persian_translation:
            return False

    if english_term in dictionary:
        dictionary[english_term].append(new_entry)
    else:
        dictionary[english_term] = [new_entry]

    save_dictionary(dictionary)
    return True


def update_rating(english_term, translation_index, new_rating):
    english_term = english_term.lower()
    translations = dictionary.get(english_term)
    translation_entry = translations[int(translation_index)]

    if "rating_no" not in translation_entry:
        translation_entry["rating_no"] = 0
    translation_entry["rating_no"] += 1

    rating = (translation_entry["rating_no"] * translation_entry["rating"] + new_rating) / (translation_entry["rating_no"] + 1)
    rating = round(rating * 2) / 2
    translation_entry["rating"] = rating

    translations = sorted(translations, key=lambda x: x["rating"], reverse=True)
    dictionary[english_term] = translations
    save_dictionary(dictionary)
