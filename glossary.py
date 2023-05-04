"""This module contains functions for loading, saving, searching, and adding to the dictionary."""
import yaml

class Glossary:
    """A class for loading, saving, searching, and adding to the dictionary"""
    def __init__(self, dictionary_file, s3, bucket_name, glossary_file_key) -> None:
        """Initialize the dictionary"""
        self.dictionary_file = dictionary_file
        self.s3 = s3
        self.bucket_name = bucket_name
        self.glossary_file_key = glossary_file_key
        self.read_from_s3()

    def read_from_s3(self):
        """Load the dictionary from S3"""
        with open(self.dictionary_file, 'wb') as file:
            self.s3.download_fileobj(self.bucket_name, self.glossary_file_key, file)

        self._load_dictionary()

    def _load_dictionary(self):
        """Load the dictionary from a YAML file"""
        with open(self.dictionary_file, "r", encoding="utf-8") as file:
            dictionary = yaml.safe_load(file)

        # sort the dictionary for each term based on the rating
        for term in dictionary:
            dictionary[term] = sorted(dictionary[term], key=lambda x: x['rating'], reverse=True)

        self.dictionary = dictionary


    def save_to_s3(self):
        """Save the dictionary to S3"""
        with open(self.dictionary_file, 'rb') as file:
            self.s3.upload_fileobj(file, self.bucket_name, self.glossary_file_key)


    def save_dictionary(self):
        """Save the dictionary to a YAML file"""
        with open(self.dictionary_file, "w", encoding="utf-8") as file:
            yaml.dump(self.dictionary, file, allow_unicode=True)

        self.save_to_s3()


    def search_dictionary(self, term):
        """Search the dictionary for a term"""
        term = term.lower()
        translations = self.dictionary.get(term)
        if translations is None:
            return None
        return [translation for translation in translations if translation.get("approved", True)]


    def add_translation(self, english_term, persian_translation):
        """Add a new translation to the dictionary"""
        english_term = english_term.lower()

        # check if the translation is a valid entry, not empty
        if not persian_translation.strip():
            return False

        new_entry = {"persian": persian_translation, "rating": 0, "approved": False}

        for entry in self.dictionary.get(english_term, []):
            if entry["persian"] == persian_translation:

                return False

        if english_term in self.dictionary:
            self.dictionary[english_term].append(new_entry)
        else:
            self.dictionary[english_term] = [new_entry]

        self.save_dictionary()
        return True


    def update_rating(self, english_term, translation_index, new_rating):
        """Update the rating of a translation"""
        english_term = english_term.lower()
        translations = self.dictionary.get(english_term)
        translation_entry = translations[int(translation_index)]

        if "rating_no" not in translation_entry:
            translation_entry["rating_no"] = 0
        translation_entry["rating_no"] += 1

        rating = (translation_entry["rating_no"] * translation_entry["rating"] + new_rating) / (translation_entry["rating_no"] + 1)
        rating = round(rating * 2) / 2
        translation_entry["rating"] = rating

        translations = sorted(translations, key=lambda x: x["rating"], reverse=True)
        self.dictionary[english_term] = translations
        self.save_dictionary()
