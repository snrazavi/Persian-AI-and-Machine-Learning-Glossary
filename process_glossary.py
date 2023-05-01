"""Sort the glossary terms in alphabetical order reading from a YAML file."""
import yaml
from collections import OrderedDict


def sort_dicts_by_key(dicts, key, reverse=False):
    """
    Sort a list of dictionaries by a key
    :param dicts: list of dictionaries
    :param key: key to sort by
    :param reverse: whether to sort in reverse order
    :return: sorted list of dictionaries
    """
    return sorted(dicts, key=lambda x: x[key], reverse=reverse)


def sort_glossary(language='en'):
    """
    Sort the glossary terms in alphabetical order reading from a YAML file
    :param language: language of the glossary
    :return: None
    """
    # read the glossary from a YAML file and sort it
    with open('Glossary.yaml', 'r', encoding='utf-8') as f:
            glossary = yaml.load(f, Loader=yaml.FullLoader)
            if language == 'en':
                # sort each dictionary entry by the English term
                sorted_glossary = sort_dicts_by_key(glossary, 'english')
            elif language == 'fa':
                sorted_glossary = sort_dicts_by_key(glossary, 'persian')
            else:
                raise ValueError('language should be either "en" or "fa"')
    
    # write the sorted glossary to a new YAML file
    output_filename = f"Glossary_sorted_{language}.yaml"
    with open(output_filename, 'w', encoding='utf-8') as f:
        yaml.dump(sorted_glossary, f, allow_unicode=True)


if __name__ == '__main__':
    sort_glossary(language='en')
    sort_glossary(language='fa')
