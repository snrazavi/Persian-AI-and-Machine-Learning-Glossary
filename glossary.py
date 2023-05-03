""" This module contains a class for storing and manipulating a glossary."""
import yaml


class Glossary:
    """
    A class for storing and manipulating a glossary.
    """
    def __init__(self, glossary_file: str ='Glossary.yaml') -> None:
        """
        Initialize the glossary
        :param glossary_file: YAML file containing the glossary
        """
        self.glossary_file = glossary_file
        self.glossary = self.read_glossary()
        self._deduplicate_glossary()

    def __len__(self) -> int:
        """
        Return the number of terms in the glossary
        :return: number of terms in the glossary
        """
        return len(self.glossary)

    @staticmethod
    def sort_dicts_by_key(dicts: list[dict], key: str, reverse: bool=False) -> list[dict]:
        """
        Sort a list of dictionaries by a key
        :param dicts: list of dictionaries
        :param key: key to sort by
        :param reverse: whether to sort in reverse order
        :return: sorted list of dictionaries
        """
        return sorted(dicts, key=lambda x: x[key], reverse=reverse)

    def _deduplicate_glossary(self) -> None:
        """
        Remove duplicate terms from the glossary
        :return: None
        """
        duplicate_found = False
        deduplicated_glossary = []
        for term in self.glossary:
            if term not in deduplicated_glossary:
                deduplicated_glossary.append(term)
            else:
                print(f"Duplicate term: {term['english']}")
                duplicate_found = True
        self.glossary = deduplicated_glossary
        if duplicate_found:
            print("Duplicate terms found in the glossary. Rewriting the glossary file...")
            self.write_glossary(self.glossary, self.glossary_file)

    def read_glossary(self) -> list[dict]:
        """
        Read the glossary from a YAML file
        :return: glossary
        """
        with open(self.glossary_file, 'r', encoding='utf-8') as file:
            glossary = yaml.load(file, Loader=yaml.FullLoader)
        return glossary

    def write_glossary(self, glossary: list[dict], glossary_file: str) -> None:
        """
        Write the glossary to a YAML file
        :param glossary: glossary
        :param glossary_file: YAML file to write the glossary to
        :return: None
        """
        with open(glossary_file, 'w', encoding='utf-8') as file:
            yaml.dump(glossary, file, allow_unicode=True)

    def sort_glossary(self, language: str='en') -> list[dict]:
        """
        Sort the glossary terms in alphabetical order reading from a YAML file
        and write the sorted glossary to a new YAML file
        :param language: language of the glossary
        :return: None
        """
        # sort the glossary terms in alphabetical order based on the language
        if language == 'en':
            sorted_glossary = self.sort_dicts_by_key(self.glossary, 'english')
        elif language == 'fa':
            sorted_glossary = self.sort_dicts_by_key(self.glossary, 'persian')
        else:
            raise ValueError('language should be either "en" or "fa"')

        return sorted_glossary
    
    def convert_glossary_format_for_ratings(self) -> list[dict]:
        """
        Convert the glossary format to the format required for ratings
        :return: glossary in the format required for ratings
        """
        glossary = []
        for entry in self.glossary:
            english = entry['english']
            persian = entry['persian']
            # split persian terms by semicolon
            persian_terms = persian.split('؛')
            translations = [{'persian': persian_term.strip(), 'rating': 0} for persian_term in persian_terms]
            glossary.append({'english': english, 'translations': translations})

        # save the glossary in the format required for ratings
        self.write_glossary(glossary, 'Glossary_for_ratings.yaml')
        return glossary


if __name__ == '__main__':
    enfa_glossary = Glossary('Glossary.yaml')
    print(f"Number of terms in the glossary: {len(enfa_glossary)}")