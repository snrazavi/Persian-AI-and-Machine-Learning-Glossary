"""Helper functions for the application"""
import difflib
from models.glossary_term import GlossaryTerm, db
from models.translation import Translation


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
        translations = [translation for translation in term_entry.translations if translation.approved]
        return sorted(enumerate(translations), key=lambda t: t[1].rating, reverse=True)

    # search for the closest match to the term
    all_terms = [glossary_term.english_term for glossary_term in GlossaryTerm.query.all()]
    closest_match = difflib.get_close_matches(glossary_term, all_terms, n=1, cutoff=0.6)
    if closest_match:
        similar_term = closest_match[0]
        translations = GlossaryTerm.query.filter_by(english_term=similar_term).first().translations
        # only return approved translations
        translations = [translation for translation in translations if translation.approved]
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
        persian_translation=persian_translation, glossary_term_id=glossary_term_id, approved=False)
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


def generate_star_rating(rating):
    """Generate a star rating based on the rating"""
    full_star = '<i class="fas fa-star"></i>'
    empty_star = '<i class="far fa-star"></i>'
    half_star = '<i class="fas fa-star-half-alt"></i>'

    full_stars = int(rating)
    half_stars = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_stars

    star_rating = full_star * full_stars + half_star * half_stars + empty_star * empty_stars
    return star_rating
