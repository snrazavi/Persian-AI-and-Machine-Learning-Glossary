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

        # # write the sorted glossary to a new YAML file
        # output_filename = f"Glossary_sorted_{language}.yaml"
        # self.write_glossary(sorted_glossary, output_filename)
