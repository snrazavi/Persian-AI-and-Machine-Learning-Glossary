""" This script is used to migrate the glossary data from the YAML file to the database. """
from application import db, GlossaryTerm, Translation, application
import yaml

# Load the YAML file
with open("Glossary_for_ratings.yaml", "r", encoding="utf-8") as f:
    glossary_data = yaml.safe_load(f)

with application.app_context():
    # db.create_all() # only create the tables if they don't exist
    # Iterate through the YAML data and create Term and Translation objects
    for english_term, translations in glossary_data.items():

        term = GlossaryTerm(english_term=english_term)
        db.session.add(term)
        db.session.flush() # flush the session to get the term id
        for translation in translations:
            try:
                persian_translation = Translation(
                    persian_translation=translation["persian"],
                    rating=translation.get("rating", 0),
                    rating_no=translation.get("rating_no", 0),
                    approved=translation.get("approved", True),
                    glossary_term_id=term.id,
                )
                db.session.add(persian_translation)
            except Exception as e:
                print(e)
                print(translation)
                print(english_term)
        
        print(f"Added {english_term} to the database")


    # Commit the changes to the database
    db.session.commit()
